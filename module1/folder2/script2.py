"""
Script to verify that introcs is installed and display a result

Author: Walker M. White
Date:   July 31, 2018
"""


try:
    import introcs
    print('Package introcs is installed!')
    print(introcs.center('We can use this',20))
    print(introcs.center('module to',20))
    print(introcs.center('center text',20))
except:
    print('Package introcs is not installed!')
    print('Consult your instructor for help.')
