def initials(n='John Smith'):
    """
    Returns: The initials <first>. <last>. of the given name.
    
    We assume that n is just two names (first and last). Middle names are
    not supported.

    Example: initials('John Smith') returns 'J. S.'
    Example: initials('Walker White') returns 'W. W.'

    Parameter n: the person's name
    Precondition: n is in the form 'first-name last-name' with one space between names.
    There are no spaces in either <first-name> or <last-name>
    """

    # names = n.split(" ")
    # first_initial = names[0][0]
    # last_initial = names[1][0]
# return f"{first_initial}. {last_initial}."

    import introcs
    # Find the first initial and assign it to 'first'
    first = n[0:1]
    # Find the position of the last initial (right after the space) and assign it to 'pos'
    pos = introcs.find_str(n, ' ')+1
    # Find the last initial and assign it to 'last'
    last = n[pos:pos+1]
    # # Compute the final answer and assign it to 'result'
    # result = first + '. ' + last + '.'
    # # Return the answer
    return last

# Test the function
if __name__ == "__main__":
    print(initials('John Smith'))
    print(initials('Walker White'))
    print(initials())
