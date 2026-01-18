"""
A simple function computing time elapsed

Author: Kate Totten
Date:   2026-01-18
"""
import datetime


def past_a_week(d1,d2):
    """
    Returns True if event d2 happens at least a week (7 days) after d1.
    
    If d1 is after d2, or d2 is less than a week after d1, this function returns False.
    Values d1 and d2 can EITHER be date objects or datetime objects.  If a date object,
    assume that it happens at midnight of that day. 
    
    Parameter d1: The first event
    Precondition: d1 is EITHER a date object or a datetime object
    
    Parameter d2: The second event
    Precondition: d2 is EITHER a date object or a datetime object
    """
    # HINT: Check the type of d1 or d2. If not a datetime, convert it for comparison
    if type(d1) == datetime.date:
        d1 = datetime.datetime.combine(d1, datetime.time())
    if type(d2) == datetime.date:
        d2 = datetime.datetime.combine(d2, datetime.time())
    return (d2 - d1).days >= 7
