"""
Module providing utility functions for this project.

These functions are general purpose utilities used by other modules in this project.
Some of these functions were exercises in early course modules and should be copied
over into this file.

The preconditions for many of these functions are quite messy.  While this makes writing 
the functions simpler (because the preconditions ensure we have less to worry about), 
enforcing these preconditions can be quite hard. That is why it is not necessary to 
enforce any of the preconditions in this module.

Author: Kate Totten
Date: 2026-01-20
"""
import csv
import json
import datetime
from dateutil.parser import parse
import pytz


def read_csv(filename):
    """
    Returns the contents read from the CSV file filename.
    
    This function reads the contents of the file filename and returns the contents as
    a 2-dimensional list. Each element of the list is a row, with the first row being
    the header. Cells in each row are all interpreted as strings; it is up to the 
    programmer to interpret this data, since CSV files contain no type information.
    
    Parameter filename: The file to read
    Precondition: filename is a string, referring to a file that exists, and that file 
    is a valid CSV file
    """
    l = []
    with open(filename, 'r') as f:
        for line in f:  
            row = line.strip().split(',')  # Split the line into items
            l.append(row)  
    
    return l


def write_csv(data,filename):
    """
    Writes the given data out as a CSV file filename.
    
    To be a proper CSV file, data must be a 2-dimensional list with the first row 
    containing only strings.  All other rows may be any Python value.  Dates are
    converted using ISO formatting. All other objects are converted to their string
    representation.
    
    Parameter data: The Python value to encode as a CSV file
    Precondition: data is a  2-dimensional list of strings
    
    Parameter filename: The file to read
    Precondition: filename is a string representing a path to a file with extension
    .csv or .CSV.  The file may or may not exist.
    """
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        for row in data:
            writer.writerow(row)


def read_json(filename):
    """
    Returns the contents read from the JSON file filename.
    
    This function reads the contents of the file filename, and will use the json module
    to covert these contents in to a Python data value.  This value will either be a
    a dictionary or a list. 
    
    Parameter filename: The file to read
    Precondition: filename is a string, referring to a file that exists, and that file 
    is a valid JSON file
    """
    f = open(filename)
    contents = f.read()
    f.close()
    result = json.loads(contents)  # Convert JSON string to Python object
    return result


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
    try:
        # Parse the timestamp
        dt = parse(timestamp)
    except:
        return None
       
    # Apply tzsource if parsed datetime has no timezone
    if dt.tzinfo is None and tzsource is not None:
        if type(tzsource) == str:
            # Use pytz to localize
            tz = pytz.timezone(tzsource)
            dt = tz.localize(dt)
        else:
            # tzsource is a datetime object - extract and localize with its timezone
            if hasattr(tzsource.tzinfo, 'localize'):
                # It's a pytz timezone - use localize
                dt = tzsource.tzinfo.localize(dt)
            else:
                # It's a fixed offset timezone - replace is safe here
                dt = dt.replace(tzinfo=tzsource.tzinfo)
        
    return dt
        



def daytime(time,daycycle):
    """
    Returns true if the time takes place during the day.
    
    A time is during the day if it is after sunrise but before sunset, as
    indicated by the daycycle dicitionary.
    
    A daycycle dictionary has keys for several years (as int).  The value for
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
    datetime objects from this set.  If the time parameter does not have a timezone,
    we assume that it is in the same timezone as the daycycle dictionary
    
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


def get_for_id(id,table):
    """
    Returns (a copy of) a row of the table with the given id.
    
    Table is a two-dimensional list where the first element of each row is an identifier
    (string).  This function searches table for the row with the matching identifier and
    returns a COPY of that row. If there is no match, this function returns None.
    
    This function is useful for extract rows from a table of pilots, a table of instructors,
    or even a table of planes.
    
    Parameter id: The id of the student or instructor
    Precondition: id is a string
    
    Parameter table: The 2-dimensional table of data
    Precondition: table is a non-empty 2-dimension list of strings
    """
    for row in table:
        #check the first column [0] in row
        if row[0] == id:
            return row[:]  # return the entire list range of that row
    
    return None  # No match for id found


