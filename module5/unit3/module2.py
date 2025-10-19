"""
A module that imports another module.

Modules can import one another.  The imported module can be a
normal python module, or one that is user-defined.  If it is
user-defined, it MUST be in the same directory of this module.

Author: Walker M. White (wmw2)
Date:   July 31, 2018
"""
# Import a standard python module
import math
x = math.cos(0)

# Import a user-defined module
import temp
y = temp.to_centigrade(32.0)
