import math
from math import floor
from math import ceil as c

localmath = math
floorval = localmath.floor(3.2)
print(floorval)

def ceil(a):
    print("LOCAL CEIL")

print(floor(3.7))
print(c(3.2))

print(math.ceil(3.2))

_import_m = __import__("math")
_import_sqrt = __import__("math", fromlist=["sqrt"]).sqrt

print(_import_m.ceil(3.2))
print(_import_sqrt(3))
