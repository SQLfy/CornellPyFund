To run the tests when working with the application:

In the Terminal, move inside the auditor folder
Run the test folder as a script to run all of the test cases
Or to run specific tests, use the folder as a module
Included in the tests folder are modules __main__.py and __init__.py.

__main__.py:

May have an input function to get information from user and a print statement to display the result
Has to be in the folder in order for the application to run
Should only contain script code; all other code, including function definitions, should go in other modules
This has been completed for you
__init__.py

Tells you exactly what you should import
Files you’ll need to work on:

utils.py: 
File and date functions
You've already finished these in previous course modules; you just need to cut and paste that work into this file
pilots.py: 
Classifies pilot skill level
Necessary to find the right weather restrictions
Hardest function in the assignment
violations.py: 
Checks for weather violations
Compare the set restrictions to the current weather
Most complex module in the project
Many functions; bulk of the work in the project
app.py: Run the application (or test it)

Optional files for an extra challenge:

endorsements.py: 
Additional flight violations
Verifies that the pilot is certified for specific plane
Not that hard; just have to learn more files
inspections.py: 
Verification of plane maintenance
This is much harder; not broken up into helpers
Only for students who want a real challenge

