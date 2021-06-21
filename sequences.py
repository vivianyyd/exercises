"""
Used this to explain recursive and explicit formulas of sequences to a student.
"""

# 5 3 1 -1  -- arithmetic, decreases by 2, start at 5
# 25 75 225 675  -- geometric, increases by 3, start at 25
import math


def recarith(n):
    """return the nth item of the geometric sequence! :)"""
    if n == 1:
        return 5
    else:
        return recarith(n - 1) * 2


def exarith(n):
    return 5 + math.pow(-2, n - 1)


print(recarith(14))
print(exarith(14))
