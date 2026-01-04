"""
Module demonstrating immutable functions on dictionaries

All of these functions make use of accumulators.

Author: Kate Totten
Date: 2026-01-04
"""


def average_grade(adict):
    """
    Returns the average grade among all students.

    The dictionary adict has netids for keys and numbers 0-100 for values.
    These represent the grades that the students got on the exam.  This function
    averages those grades and returns a value.

    Examples:
        average_grade({'wmw2' : 55, 'abc3' : 90, 'jms45': 86}) returns (55+90+86)/3 = 77
        average_grade({'wmw2' : 55}) returns 55
        average_grade({}) returns 0
    
    Parameter adict: the dictionary of grades
    Precondition: adict is dictionary mapping strings to ints
    """
    if len(adict) == 0:
        return 0
    
    total = 0
    #dictionary values can be accessed directly
    for grade in adict.values():
        total = total + grade
    avg = total / len(adict)
    
    return avg


def letter_grades(adict):
    """
    Returns a new dictionary with the letter grades for each student.
    
    The dictionary adict has netids for keys and numbers 0-100 for values. These
    represent the grades that the students got on the exam. This function returns a 
    new dictionary with netids for keys and letter grades (strings) for values.
    
    Our cut-off is 90 for an A, 80 for a B, 70 for a C, 60 for a D. Anything below 60 
    is an F.
    
    Examples:  
        letter_grades({'wmw2' : 55, 'abc3' : 90, 'jms45': 86}) returns
            {'wmw2' : 'F, 'abc3' : 'A', 'jms45': 'B'}.
        letter_grades({}) returns {}
    
    Parameter adict: the dictionary of grades
    Precondition: adict is dictionary mapping strings to ints
    """
    alleval = {}

    for netid, grade in adict.items():
        if grade >= 90:
            letter = 'A'
        elif grade >= 80:
            letter = 'B'
        elif grade >= 70:
            letter = 'C'
        elif grade >= 60:
            letter = 'D'
        else:
            letter = 'F'
        
        alleval[netid] = letter

    return alleval

