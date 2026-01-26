"""
Module to check violations for a flight lesson.

This module processes the primary violations, which are violations of weather restrictions. 
Weather restrictions express the minimum conditions that a pilot is allowed to fly in.  
So if a pilot has a ceiling minimum of 2000 feet, and there is cloud cover at 1500 feet, 
the pilot should not fly.To understand weather minimums, you have to integrate three 
different files: daycycle.json (for sunrise and sunset), weather.json (for hourly weather 
observations at the airport), and minimums.csv (for the schools minimums set by agreement 
with the insurance agency). You should look at those files BRIEFLY to familiarize yourself 
with them.

This module can get overwhelming if you panic and think too much about the big picture.  
Like a good software developer, you should focus on the specifications and do a little
at a time.  While these functions may seem like they require a lot of FAA knowledge, all
of the information you need is in the specifications. They are complex specifications,
but all of the information you need is there.  Combined with the provided unit tests
in tests.py, this assignment is very doable.

It may seem weird that these functions only check weather conditions at the time of 
takeoff and not the entire time the flight is in the air.  This is standard procedure 
for this insurance company.  The school is only liable if they let a pilot take off in 
the wrong conditions.  If the pilot stays up in adverse conditions, responsibility shifts 
to the pilot.

The preconditions for many of these functions are quite messy.  While this makes writing 
the functions simpler (because the preconditions ensure we have less to worry about), 
enforcing these preconditions can be quite hard. That is why it is not necessary to 
enforce any of the preconditions in this module.

Author: Kate Totten
Date: 2026-01-21
"""
import utils
import pilots
import os.path
import json
import csv
import datetime
from dateutil.parser import parse
import pytz


# WEATHER FUNCTIONS
def bad_visibility(visibility,minimum):
    """
    Returns True if the visibility measurement violates the minimum, False otherwise
    
    A valid visibility measurement is EITHER the string 'unavailable', or a dictionary 
    with (up to) four values: 'minimum', 'maximum',  'prevailing', and 'units'. Only 
    'prevailing' and 'units' are required; the other two are optional. The units may be 
    'FT' (feet) or 'SM' for (statute) miles, and explain how to interpret other three 
    fields, which are all floats.
    
    This function should compare ths visibility 'minimum' (if it exists) against the 
    minimum parameter. Else it compares the 'prevailing' visibility. This function returns
    True if minimum is more than the measurement. If the visibility is 'unavailable', 
    then this function returns True (indicating bad record keeping).
    
    Example: Suppose we have the following visibility measurement.
        
        {
            "prevailing": 21120.0,
            "minimum": 1400.0,
            "maximum": 21120.0,
            "units": "FT"
        }
    
    Given the above measurement, this function returns True if visibility is 0.25 (miles)
    and False if it is 1.
    
    Parameter visibility: The visibility information
    Precondition: visibility is a valid visibility measurement, as described above.
    (e.g. either a dictionary or the string 'unavailable')
    
    Parameter minimum: The minimum allowed visibility (in statute miles)
    Precondition: minimum is a float or int
    """
    # If visibility is unavailable; bad visibility
    if visibility == 'unavailable':
        return True
    
    # Determine which visibility value to use
    if 'minimum' in visibility:
        vis_value = visibility['minimum']
    else:
        vis_value = visibility['prevailing']
    
    # Convert to statute miles if needed
    if visibility['units'] == 'FT':
        # Convert feet to miles (5280 feet = 1 mile)
        vis_in_miles = vis_value / 5280.0
    else:  # units == 'SM'
        vis_in_miles = vis_value
    
    # Return True if actual visibility is LESS than the minimum i.e., bad visibility
    return vis_in_miles < minimum


def bad_winds(winds,maxwind,maxcross):
    """
    Returns True if the wind measurement violates the maximums, False otherwise
    
    A valid wind measurement is EITHER the string 'calm', the string 'unavailable' or 
    a dictionary with (up to) four values: 'speed', 'crosswind', 'gusts', and 'units'. 
    Only 'speed' and 'units' are required if it is a dictionary; the other two are 
    optional. The units are either be 'KT' (knots) or 'MPS' (meters per second), and 
    explain how to interpret other three fields, which are all floats.
    
    This function should compare 'speed' or 'gusts' against the maxwind parameter
    (whichever is worse) and 'crosswind' against the maxcross. If either measurement is greater
    than the allowed maximum, this function returns True.
    
    If the winds are 'calm', then this function always returns False. If the winds are
    'unavailable', then this function returns True (indicating bad record keeping).
    
    For conversion information, 1 MPS is roughly 1.94384 knots.
    
    Example: Suppose we have the following wind measurement.
        
        {
            "speed": 12.0,
            "crosswind": 10.0,
            "gusts": 18.0,
            "units": "KT"
        }
    
    Given the above measurement, this function returns True if maxwind is 15 or maxcross is 5.
    If both maxwind is 20 and maxcross is 10, it returns False.  (If 'units' were 'MPS'
    it would be false in both cases).
    
    Parameter winds: The wind speed information
    Precondition: winds is a valid wind measurement, as described above.
    (e.g. either a dictionary, the string 'calm', or the string 'unavailable')
    
    Parameter maxwind: The maximum allowable wind speed (in knots)
    Precondition: maxwind is a float or int
    
    Parameter maxcross: The maximum allowable crosswind speed (in knots)
    Precondition: maxcross is a float or int
    """
    # If winds are unavailable; bad winds
    if type(winds) == str:
        if winds == 'calm':
            return False
        if winds == 'unavailable':
            return True

    # If values are in MPS do a conversion: 1 MPS is roughly 1.94384 knots.
    elif type(winds) == dict:
        if winds['units'] == 'MPS':
            speed_value = winds['speed'] * 1.94384
            crosswind_value = winds['crosswind'] * 1.94384
        else:  # winds['units'] == 'KT'
            speed_value = winds['speed']
            crosswind_value = winds['crosswind']
    
    # Check for gusts - use gust speed if present, otherwise regular speed
    if 'gusts' in winds:
        wind_speed_or_gusts = winds['gusts']
    else:
        wind_speed_or_gusts = speed_value
    
    # Now determine which wind value is in violation
    if wind_speed_or_gusts > maxwind:
        return True
    elif crosswind_value > maxcross:
        return True
    
    # If we get here, winds are acceptable
    return False


def bad_ceiling(ceiling,minimum):
    """
    Returns True if the ceiling measurement violates the minimum, False otherwise
    
    A valid ceiling measurement is EITHER the string 'clear', the string 'unavailable', 
    or a list of cloud layer measurements. A cloud layer measurement is a dictionary with 
    three required keys: 'type', 'height', and 'units'.  Type is one of 'a few', 
    'scattered', 'broken', 'overcast', or 'indefinite ceiling'. The value 'units' must 
    be 'FT', and specifies the units for the float associated with 'height'.
    
    If the ceiling is 'clear', then this function always returns False. If the ceiling 
    is 'unavailable', then this function returns True (indicating bad record keeping).
    Otherwise, it compares the minimum allowed ceiling against the lowest cloud layer 
    that is either 'broken', 'overcast', or 'indefinite ceiling'. If the only type of
    cloud layer is 'a few' or 'scattered', then this function should return False.
    
    Example: Suppose we have the following ceiling measurement.
        
        [
            {
                "cover": "clouds",
                "type": "scattered",
                "height": 700.0,
                "units": "FT"
            },
            {
                "type": "overcast",
                "height": 1200.0,
                "units": "FT"
            }
        ]
    
    Given the above measurement, this function returns True if minimum is 2000,
    but False if it is 1000.
    
    Parameter ceiling: The ceiling information
    Precondition: ceiling is a valid ceiling measurement, as described above.
    (e.g. either a dictionary, the string 'clear', or the string 'unavailable')
        
    Parameter minimum: The minimum allowed ceiling (in feet)
    Precondition: minimum is a float or int
    """

    cloudy_list = ['broken', 'overcast', 'indefinite ceiling']
    
    # Handle string cases
    if type(ceiling) == str:
        if ceiling == 'clear':
            return False
        if ceiling == 'unavailable':
            return True
    
    # Handle list of cloud layers
    elif type(ceiling) == list:
        # Find the lowest height among problematic cloud types
        lowest_bad_height = None
        
        for layer in ceiling:
            # Only check layers that are in the cloudy_list
            if layer['type'] in cloudy_list:
                height = layer['height']
                
                # Track the lowest height we find
                if lowest_bad_height is None or height < lowest_bad_height:
                    lowest_bad_height = height
        
        # If we found a cloudy layer, check if it violates minimum
        if lowest_bad_height is not None:
            return lowest_bad_height < minimum
        
        # If only 'a few' or 'scattered' clouds, return False
        return False



def get_weather_report(takeoff,weather):
    """
    Returns the most recent weather report at or before take-off.
    
    The weather is a dictionary whose keys are ISO formatted timestamps and whose values 
    are weather reports.  For example, here is an example of a (small portion of) a
    weather dictionary:
        
        {
            "2017-04-21T08:00:00-04:00": {
                "visibility": {
                "prevailing": 10.0,
                "units": "SM"
            },
            "wind": {
                "speed": 13.0,
                "crosswind": 2.0,
                "units": "KT"
            },
            "temperature": {
                "value": 13.9,
                "units": "C"
            },
            "sky": [
                {
                    "cover": "clouds",
                    "type": "broken",
                    "height": 700.0,
                    "units": "FT"
                }
            ],
            "code": "201704211056Z"
        },
        "2017-04-21T07:00:00-04:00": {
            "visibility": {
                "prevailing": 10.0,
                "units": "SM"
            },
            "wind": {
                "speed": 13.0,
                "crosswind": 2.0,
                "units": "KT"
            },
            "temperature": {
                "value": 13.9,
                "units": "C"
            },
            "sky": [
                {
                    "type": "overcast",
                    "height": 700.0,
                    "units": "FT"
                }
            ],
            "code": "201704210956Z"
        }
        ...
    },
    
    If there is a report whose timestamp matches the ISO representation of takeoff, 
    this function uses that report.  Otherwise it searches the dictionary for the most
    recent report before (but not equal to) takeoff.  If there is no such report, it
    returns None.
    
    Example: If takeoff was as 8 am on April 21, 2017 (Eastern), this function returns 
    the value for key '2017-04-21T08:00:00-04:00'.  If there is no additional report at
    9 am, a 9 am takeoff would use this value as well.
    
    Parameter takeoff: The takeoff time
    Precondition: takeoff is a datetime object
    
    Paramater weather: The weather report dictionary 
    Precondition: weather is a dictionary formatted as described above
    """
    # HINT: Looping through the dictionary is VERY slow because it is so large
    # You should convert the takeoff time to an ISO string and search for that first.
    # Only loop through the dictionary as a back-up if that fails.
    
    target_str = takeoff.isoformat()

    # Try exact match first
    if target_str in weather:
        return weather[target_str]

    # No exact match - find closest BEFORE takeoff
    # Convert to UTC for comparison
    takeoff_utc = takeoff.astimezone(pytz.UTC)

    closest_key = None
    closest_time_utc = None

    for key in weather:
        try:
            key_time = parse(key)
            key_time_utc = key_time.astimezone(pytz.UTC)
        
            # Only consider times BEFORE takeoff
            if key_time_utc < takeoff_utc:
                # Keep the MOST RECENT in UTC
                if closest_time_utc is None or key_time_utc > closest_time_utc:
                    closest_time_utc = key_time_utc
                    closest_key = key
        except Exception as e:
            #print(f"Error parsing {key}: {e}")
            continue

    #print(f"\nFINAL RESULT: {closest_key}")
    #if closest_key:
    #    print(f"Code: {weather[closest_key].get('code', 'N/A')}")

    if closest_key:
        return weather[closest_key]
    else:
        return None


def get_weather_violation(weather,minimums):
    """
    Returns a string representing the type of weather violation (empty string if flight is ok)
    
    The weather reading is a dictionary with the keys: 'visibility', 'wind', and 'sky'.
    These correspond to a visibility, wind, and ceiling measurement, respectively. It
    may have other keys as well, but these can be ignored. For example, this is a possible 
    weather value:
        
        {
            "visibility": {
                "prevailing": 21120.0,
                "minimum": 1400.0,
                "maximum": 21120.0,
                "units": "FT"
            },
            "wind": {
                "speed": 12.0,
                "crosswind": 3.0,
                "gusts": 18.0,
                "units": "KT"
            },
            "temperature": {
                "value": -15.6,
                "units": "C"
            },
            "sky": [
                {
                    "cover": "clouds",
                    "type": "broken",
                    "height": 2100.0,
                    "units": "FT"
                }
            ],
            "weather": [
                "light snow"
            ]
        }
    
    The minimums is a list of the four minimums ceiling, visibility, and max windspeed,
    and max crosswind speed in that order.  Ceiling is in feet, visibility is in statute
    miles, max wind and cross wind speed are both in knots. For example, 
    [3000.0,10.0,20.0,8.0] is a potential minimums list.
    
    This function uses bad_visibility, bad_winds, and bad_ceiling as helpers. It returns
    'Visibility' if the only problem is bad visibility, 'Winds' if the only problem is 
    wind, and 'Ceiling' if the only problem is the ceiling.  If there are multiple
    problems, it returns 'Weather', It returns 'Unknown' if no weather reading is 
    available (e.g. weather is None).  Finally, it returns '' (the empty string) if 
    the weather is fine and there are no violations.
    
    Parameter weather: The weather measure
    Precondition: weather is dictionary containing a visibility, wind, and ceiling measurement,
    or None if no weather reading is available.
    
    Parameter minimums: The safety minimums for ceiling, visibility, wind, and crosswind
    Precondition: minimums is a list of four floats
    """
    #Example
    #[ceiling,visibility, max windspeed,max crosswind speed]
    #minimums = [3000.0,10.0,20.0,8.0] 
    # If no weather reading available
    if weather is None:
        return 'Unknown'
    
    # Extract minimums from the list
    min_ceiling = minimums[0]
    min_visibility = minimums[1]
    max_windspeed = minimums[2]
    max_crosswind = minimums[3]
    
    # Check each weather component
    has_bad_visibility = bad_visibility(weather['visibility'], min_visibility)
    has_bad_winds = bad_winds(weather['wind'], max_windspeed, max_crosswind)
    has_bad_ceiling = bad_ceiling(weather['sky'], min_ceiling)
    
    # Count how many violations we have
    violation_count = 0
    violation_type = ''
    
    if has_bad_visibility:
        violation_count += 1
        violation_type = 'Visibility'
    
    if has_bad_winds:
        violation_count += 1
        violation_type = 'Winds'
    
    if has_bad_ceiling:
        violation_count += 1
        violation_type = 'Ceiling'
    
    # Return appropriate result based on violation count
    if violation_count == 0:
        return ''  # No violations
    elif violation_count == 1:
        return violation_type  # Single violation
    else:
        return 'Weather'  # Multiple violations




# FILES TO AUDIT
# Sunrise and sunset
DAYCYCLE = 'daycycle.json'
# Hourly weather observations
WEATHER  = 'weather.json'
# The list of insurance-mandated minimums
MINIMUMS = 'minimums.csv'
# The list of all registered students in the flight school
STUDENTS = 'students.csv'
# The list of all take-offs (and landings)
LESSONS  = 'lessons.csv'


def list_weather_violations(directory):
    """
    Returns the (annotated) list of flight reservations that violate weather minimums.
    
    This function reads the data files in the given directory (the data files are all
    identified by the constants defined above in this module).  It loops through the
    list of flight lessons (in lessons.csv), identifying those takeoffs for which
    get_weather_violation() is not the empty string.
    
    This function returns a list that contains a copy of each violating lesson, together 
    with the violation appended to the lesson.
    
    Example: Suppose that the lessons
        
        S00687  548QR  I061  2017-01-08T14:00:00-05:00  2017-01-08T16:00:00-05:00  VFR  Pattern
        S00758  548QR  I072  2017-01-08T09:00:00-05:00  2017-01-08T11:00:00-05:00  VFR  Pattern
        S00971  426JQ  I072  2017-01-12T13:00:00-05:00  2017-01-12T15:00:00-05:00  VFR  Pattern
    
    violate for reasons of 'Winds', 'Visibility', and 'Ceiling', respectively (and are the
    only violations).  Then this function will return the 2d list
        
        [[S00687, 548QR, I061, 2017-01-08T14:00:00-05:00, 2017-01-08T16:00:00-05:00, VFR, Pattern, Winds],
         [S00758, 548QR, I072, 2017-01-08T09:00:00-05:00, 2017-01-08T11:00:00-05:00, VFR, Pattern, Visibility],
         [S00971, 426JQ, I072, 2017-01-12T13:00:00-05:00, 2017-01-12T15:00:00-05:00, VFR, Pattern, Ceiling]]
    
    REMEMBER: VFR flights are subject to minimums with VMC in the row while IFR flights 
    are subject to minimums with IMC in the row.  The examples above are all VFR flights.
    If we changed the second lesson to
    
        S00758, 548QR, I072, 2017-01-08T09:00:00-05:00, 2017-01-08T11:00:00-05:00, IFR, Pattern
    
    then it is possible it is no longer a visibility violation because it is subject to
    a different set of minimums.
    
    Parameter directory: The directory of files to audit
    Precondition: directory is the name of a directory containing the files 'daycycle.json',
    'weather.json', 'minimums.csv', 'students.csv', and 'lessons.csv'
    """
    # Load in all of the files
    
    # For each of the lessons
        # Get the takeoff time
        # Get the pilot credentials
        # Get the pilot minimums
        # Get the weather conditions
        # Check for a violation and add to result if so
    
    # for files in directory load the files into the listed file names
    # check if the file is a csv or a json file

    #This function returns a list that contains a copy of each violating lesson, together 
    #with the violation appended to the lesson.

    #import os
    #import utils
    #import pilots

    filemap = {
    'minimums.csv':'MINIMUMS', 
    'students.csv':'STUDENTS', 
    'lessons.csv':'LESSONS',
    'daycycle.json':'DAYCYCLE', 
    'weather.json':'WEATHER'
    }
    data = {}
    lesson_violated = []
    return_violation = []
    #directory = '/home/codio/workspace/KITH-2017'

    # Loop through files in directory
    for root, dirs, files in os.walk(directory):
        for filename in files:
        # Skip files not in our mapping
            if filename not in filemap:
                continue
            filepath = os.path.join(root, filename)
            namemap = filemap[filename] #assign filemap values e.g. 'LESSIONS'
        
            # Read based on file type
            if filename.endswith('.csv'):
                data[namemap] = utils.read_csv(filepath)
            elif filename.endswith('.json'):
                data[namemap] = utils.read_json(filepath)
        
            #print(f'Loaded {filename} as {namemap}' into data dictionary)

    for lesson in data['LESSONS'][1:]:
        #print(lesson)
        takeoff_str = lesson[3]  # 3rd item from THIS lesson
        takeoff = utils.str_to_time(takeoff_str)

        student_id = lesson[0]  # 0th item from THIS lesson
        area = lesson[6]
        instructor = lesson[2]
        lesson_vfr_str = lesson[5]

        # Convert VFR string to boolean
        vfr = (lesson_vfr_str == 'VFR')  # True if Flight VFR rated, False if IFR
    
        # Is instructor is present (not empty string)
        instructed = (instructor != '')
    
        #print(f'area: {area}, instructor: {instructor}, vfr: {vfr}')

        # ====== get student record =============
        student = None
        for s in data['STUDENTS'][1:]:  # Skip header
            if s[0] == student_id:  # Match on student ID (column 0)
                student = s
                break
    
        if student is None:
            #print(f'Student {student_id} not found!')
            continue
    
        # ====== get credentials =============
        #print(f'Takeoff: {takeoff} Student Id: {student_id}')
        pilot_cred = pilots.get_certification(takeoff, student)
        #print(f'pilot_cred = {pilot_cred}')

        # ====== get daytime ==================
        lesson_daytime = utils.daytime(takeoff, data['DAYCYCLE'])
        #print(f'lesson_daytime: {lesson_daytime}')

        # ====== get pilot minimums ===========
        #returns
        #[best_ceiling, best_visibility, best_wind, best_crosswind]
        pilot_minimums = pilots.get_minimums(
        pilot_cred,      # cert
        area,            # area
        instructed,      # boolean instructor present
        vfr,             # boolean flight lesson rating
        lesson_daytime,  # boolean day or night lesson
        data['MINIMUMS'] # minimums table
        )
        #print(f'pilot_minimums: {pilot_minimums}')

        # ====== get weather for takeoff ===========

        #get_weather_report(takeoff,weather)
        takeoff_key = takeoff_str  # or format it to match your weather keys
        weather = get_weather_report(takeoff, data['WEATHER'])

        # ====== get weather violations ===========
        violation = ''
        if pilot_minimums is not None and weather is not None:
            violation = get_weather_violation(weather, pilot_minimums)
            #print(f'violation: {violation}')

        # Add result to list
        if violation != '':
            violated_lesson = lesson + [violation]  # Append violation to lesson
            lesson_violated.append(violated_lesson)
    
    return lesson_violated



