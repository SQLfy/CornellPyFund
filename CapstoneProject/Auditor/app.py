"""
Module that validates the flight school's records.

This is the primary module that does all of the work. It loads the files, loops through
the lessons, and searches for any takeoffs that violate insurance requirements.

Technically, we could have put many of these functions in __main__.py.  That is the
main module of this application anyway.  However, for testing purposes we want all
functions in modules and we only want script code in the file __main__.py

Author: Kate Totten
Date: 2026-01-20
"""
import utils
import tests
import os.path
import violations

import sys

# Uncomment for the extra credit
#import endorsements
#import inspections


def discover_violations(directory,output):
    """
    Searches the dataset directory for any flight lessons that violate the regulations.
    
    This function will call list_weather_violations() to get the list of weather violations.
    If list_endorsment_violations (optional) is completed, it will call that too, as
    well as list_inspection_violations.  It will concatenate all of these 2d lists
    into a single 2d list of violations (so a flight may be listed more than once for
    each of the three types of violations).
    
    If the parameter output is not None, it will create the CSV file with name output
    and write the 2d list of violations to this file.  This CSV file should have the
    following header:
    
        STUDENT,AIRPLANE,INSTRUCTOR,TAKEOFF,LANDING,FILED,AREA,REASON
    
    Regardless of whether output is None, this function will print out the number of
    violations, as follows:
    
        '23 violations found.'
    
    If no violations are found, it will say
    
        'No violations found.'
    
    Parameter directory: The directory of files to audit
    Precondition: directory is the name of a directory containing the files 'daycycle.json',
    'weather.json', 'minimums.csv', 'students.csv', 'teachers.csv', 'lessons.csv',
    'fleet.csv', and 'repairs.csv'.
    
    Parameter output: The CSV file to store the results
    Precondition: output is None or a string that is a valid file name
    """
    #header for output
    header = ['STUDENT','AIRPLANE','INSTRUCTOR','TAKEOFF','LANDING','FILED','AREA','REASON']
    all_violations = []
    weather_violations = []
    violation_ct = 0
    #full_path = os.path.join(directory, item)
    #for item in os.listdir(directory):

    # File map to check for required files
    # File map to check for required files
    filemap = {
        'minimums.csv': 'MINIMUMS', 
        'students.csv': 'STUDENTS', 
        'lessons.csv': 'LESSONS',
        'daycycle.json': 'DAYCYCLE', 
        'weather.json': 'WEATHER'
    }
    isfile_folder = all(os.path.exists(os.path.join(directory, filename)) 
                for filename in filemap.keys())

    if isfile_folder:
        # Process this directory directly
        weather_violations = violations.list_weather_violations(directory)
        all_violations.extend(weather_violations)

    else:
        # Look for subdirectories that contain the files
        for item in os.listdir(directory):
            full_path = os.path.join(directory, item)
            
            if os.path.isdir(full_path):
                # Check if THIS subdirectory has all required files
                isfile_folder = all(os.path.exists(os.path.join(full_path, filename)) 
                                   for filename in filemap.keys())
                
                if isfile_folder:
                    weather_violations = violations.list_weather_violations(full_path)
                    all_violations.extend(weather_violations)
    
    # Count violations
    violation_ct = len(all_violations)

    #======== create output file ==============
    if output is not None:
        # Write violations to CSV file
        utils.write_csv([header] + all_violations, output)

    #========= print to screen regardless of output file requirements  
    
    if violation_ct == 0:
        print(f'No violations found.')
    elif violation_ct == 1:
        print(f'{violation_ct} violation found.')
    else:
        print(f'{violation_ct} violations found.')
    
    return all_violations


def execute(args):
    """
    Executes the application or prints an error message if executed incorrectly.
    
    The arguments to the application (EXCLUDING the application name) are provided to
    the list args. This list should contain either 1 or 2 elements.  If there is one
    element, it should be the name of the data set folder or the value '--test'.  If
    there are two elements, the first should be the data set folder and the second
    should be the name of a CSV file (for output of the results).
    
    If the user calls this script incorrectly (with the wrong number of arguments), this
    function prints:
    
        Usage: python auditor dataset [output.csv]
    
    This function does not do much error checking beyond counting the number of arguments.
    
    Parameter args: The command line arguments for the application (minus the application name)
    Precondition: args is a list of strings
    """
    
    # Handle the special case: just '--test'
    if len(args) == 1 and args[0] == '--test':
        tests.test_all()
        return

    # Check for correct number of arguments
    if len(args) == 0 or len(args) > 2:
        print('Usage: python auditor dataset [output.csv]')
        return

    # Check if '--test' appears anywhere in a list of args (invalid)
    if '--test' in args:
        print('Usage: python auditor dataset [output.csv]')
        return

    # Happy path case: 1 or 2 arguments
    if len(args) == 1:
        # Just dataset, no output file
        dataset = args[0]
        discover_violations(dataset, None)
    elif len(args) == 2:
        # Dataset and output file
        dataset = args[0]
        output_file = args[1]
        discover_violations(dataset, output_file)
