"""
A module containing several random strings.

This is to check if the student can import the right module, even though there are
several different modules with the same name.

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


# Create the variables
x = rand_string(16,50)
y = rand_string(16,100)