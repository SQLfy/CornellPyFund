"""
Script to display a not-so-random string.

This is to check if the student can find the right folder, even though there are different
files all of the same name in each folder.

Author: Walker M. White
Date:   July 31, 2018
"""


def rand_string(size,seed=None):
    """
    Returns a random ASCII string of size elements.
    
    If seed is omitted or None, the current system time is used.
    
    Parameter size: The number of elements in the string
    Precondition: size is an int >= 0 
    
    Parameter seed: The random number seed
    Precondition: seed is an int,str, bytes, or None
    """
    import random
    random.seed(seed)
    result = []
    for x in range(size):
        value = random.randint(32,126)
        result.append(chr(value))
    return ''.join(result)


# This version
print("Random string:",rand_string(16,50))