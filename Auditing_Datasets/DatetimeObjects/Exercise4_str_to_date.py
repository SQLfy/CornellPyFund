"""
Functions for parsing time values from text.  

While these functions are similar to functions found in the assignment, they 
are missing timezone information.  The next exercise will modify these 
functions to make them compatible with the assignment.

Author: Kate Totten
Date:   2024-06-18
"""
from dateutil.parser import parse
import datetime

def str_to_time(timestamp):
    """
    Returns the datetime object for the given timestamp (or None if the stamp is invalid)
    
    This function should just use the parse function in dateutil.parser to convert the
    timestamp to a datetime object.  If it is not a valid date (so the parser crashes), 
    this function should return None.
    
    Parameter timestamp: The time stamp to convert
    Precondition: timestamp is a string
    """
    # Hint: Use a try-except to return None if parsing fails
    #timestamp = datetime.datetime(2016,4,15)
    try:
        return parse(timestamp)
    except:
        return None


def sunset(date,daycycle):
    """
    Returns the sunset datetime (day and time) for the given date
    
    This function looks up the sunset from the given daycycle dictionary. If the
    daycycle dictionary is missing the necessary information, this function 
    returns the value None.
    
    A daycycle dictionary has keys for several years (as int).  The value for each year
    is also a dictionary, taking strings of the form 'mm-dd'.  The value for that key 
    is a THIRD dictionary, with two keys "sunrise" and "sunset".  The value for each of 
    those two keys is a string in 24-hour time format.
    
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
    
    Parameter date: The date to check
    Precondition: date is a date object
    
    Parameter daycycle: The daycycle dictionary
    Precondition: daycycle is a valid daycycle dictionary, as described above
    """
    # HINT: ISO FORMAT IS 'yyyy-mm-ddThh:mm'.  Find the sunset value by constructing a
    # string in ISO format and calling str_to_time.
                 

    try:
        year_key = str(date.year)
        date_key = date.strftime("%m-%d")  # Note: "mm-dd" format per docstring
        sunset_str = daycycle[year_key][date_key]["sunset"]
        iso_str = f"{date.strftime('%Y-%m-%d')}T{sunset_str}"
        return str_to_time(iso_str)
    
    except:
        return None


if __name__ == "__main__":
    print(str_to_time("2024-06-18 14:30"))
    print(str_to_time("invalid date"))

