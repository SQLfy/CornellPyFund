"""
Functions for parsing time values and determining daylight hours.

Both of these functions will be used in the main project.  You should hold on to them.

Author: Kate Totten
Date:   2026-01-18
"""
from dateutil.parser import parse
from dateutil import tz
import pytz
import datetime


def str_to_time(timestamp,tzsource=None):
    """
    Returns the datetime object for the given timestamp (or None if timestamp is 
    invalid).
    
    This function should just use the parse function in dateutil.parser to
    convert the timestamp to a datetime object.  If it is not a valid date (so
    the parser crashes), this function should return None.
    
    If the timestamp has a time zone, then it should keep that time zone even if
    the value for tzsource is not None.  Otherwise, if timestamp has no time zone 
    and tzsource is not None, then this function will use tzsource to assign 
    a time zone to the new datetime object.
    
    The value for tzsource can be None, a string, or a datetime object.  If it 
    is a string, it will be the name of a time zone, and it should localize the 
    timestamp.  If it is another datetime, then the datetime object created from 
    timestamp should get the same time zone as tzsource.
    
    Parameter timestamp: The time stamp to convert
    Precondition: timestamp is a string
    
    Parameter tzsource: The time zone to use (OPTIONAL)
    Precondition: tzsource is either None, a string naming a valid time zone,
    or a datetime object.
    """
    # HINT: Use the code from the previous exercise and add time zone handling.
    # Use localize if tzsource is a string; otherwise replace the time zone if not None
    #timestamp = "2024-06-18 14:30"
    #tzsource = "-5:00"
    try:
        dt = parse(timestamp)
    except:
        return None
    try:    
        # Apply tzsource if the parsed datetime has no timezone
        if dt.tzinfo is None and tzsource is not None:
            if type(tzsource) == str:
                # localize if it is a tz name
                dt = dt.replace(tzinfo=tz.gettz(tzsource))
            elif type(tzsource) == datetime.datetime:
                # tzsource converts to tz offset copy its timezone
                dt = dt.replace(tzinfo=tzsource.tzinfo)
        
        return dt
    except:
        return None



def daytime(time,daycycle):
    """
    Returns True if the time takes place during the day, False otherwise (and 
    returns None if a key does not exist in the dictionary).
    
    A time is during the day if it is after sunrise but before sunset, as
    indicated by the daycycle dictionary.
    
    A daycycle dictionary has keys for several years (as strings).  The value for
    each year is also a dictionary, taking strings of the form 'mm-dd'.  The
    value for that key is a THIRD dictionary, with two keys "sunrise" and
    "sunset".  The value for each of those two keys is a string in 24-hour
    time format.
    
    For example, here is what part of a daycycle dictionary might look like:
    
        "2015": {
            "01-01": {
                "sunrise": "07:35",
                "sunset":  "16:44"
            },
            "01-02": {
                "sunrise": "07:36",
                "sunset":  "16:45"
            },
            ...
        }
    
    In addition, the daycycle dictionary has a key 'timezone' that expresses the
    timezone as a string. This function uses that timezone when constructing
    datetime objects using data from the daycycle dictionary.  Also, if the time
    parameter does not have a timezone, we assume that it is in the same timezone 
    as the daycycle dictionary.
    
    Parameter time: The time to check
    Precondition: time is a datetime object
    
    Parameter daycycle: The daycycle dictionary
    Precondition: daycycle is a valid daycycle dictionary, as described above
    """
    # HINT: Use the code from the previous exercise to get sunset AND sunrise
    # Add a timezone to time if one is missing (the one from the daycycle)
    
    #default tz
    tz_name = daycycle['timezone']
    target_tz = pytz.timezone(tz_name)  

    try:
        # Convert input time to daycycle's timezone
        if time.tzinfo is None:
            time = target_tz.localize(time)
        else:
            time = time.astimezone(target_tz)
        
        year_key = str(time.year)
        date_key = time.strftime("%m-%d")
        sunrise_str = daycycle[year_key][date_key]["sunrise"]
        sunset_str = daycycle[year_key][date_key]["sunset"]
        
        date_str = time.strftime("%Y-%m-%d")
        sunrise_iso = f"{date_str}T{sunrise_str}"
        sunset_iso = f"{date_str}T{sunset_str}"
        
        sunrise_dt = target_tz.localize(parse(sunrise_iso))  
        sunset_dt = target_tz.localize(parse(sunset_iso))  
        
        return sunrise_dt < time < sunset_dt
        
    except:
        return None
