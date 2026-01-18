"""
Functions for simple reading to and writing from a file.

Author: Kate Totten
Date:   2025-01-16
"""
import os

def count_lines(filepath):
    """
    Returns the number of lines in the given file.
    
    Lines are separated by the '\n' character, which is standard for Unix files.
    
    Parameter filepath: The file to be read
    Precondition: filepath is a string with the FULL PATH to a text file
    """
    # HINT: Remember, you can use a file in a for-loop
    import os            # Implement me

    line_ct = 0
    #filepath = '/home/codio/workspace/exercise1/files/readfile1.txt'
    with open(filepath, 'r') as f:
        for line in f:  
            #print(line.strip()) 
            if "\n" in line:
                ct = 1
            line_ct = line_ct + 1  
      
    #print(line_ct)
    return line_ct


def write_numbers(filepath,n):
    """
    Writes the numbers 0..n-1 to a file.
    
    Each number is on a line by itself.  So the first line of the file is 0,
    the second line is 1, and so on. Lines are separated by the '\n' character, 
    which is standard for Unix files.  The last line (the one with the number
    n-1) should NOT end in '\n'
    
    Parameter filepath: The file to be written
    Precondition: filepath is a string with the FULL PATH to a text file
    
    Parameter n: The number of lines to write
    Precondition: n is an int > 0.
    """
    # HINT: You can only write strings to a file, so convert the numbers first
    #filepath = '/home/codio/workspace/exercise1/files/outputfile1.txt'
    with open(filepath, 'w') as f:
        for i in range(n):
            if i < n - 1:  # Not the last line
                f.write(str(i) + '\n')
            else:  # Last line- no newline
                f.write(str(i))

