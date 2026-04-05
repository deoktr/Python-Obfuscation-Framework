import math
import itertools


def make_multiplier(factor):
    def multiply(x):
        return x * factor

    return multiply


double = make_multiplier(2)
triple = make_multiplier(3)

print(double(5))
print(triple(4))

# Generator expression
squares_gen = (i * i for i in range(5))
print(list(squares_gen))

# Multi-line string
description = """This is a
multi-line string
with three lines"""
print(len(description.split("\n")))

# Stdlib: math
print(math.floor(3.7))
print(math.ceil(3.2))

# Stdlib: itertools
pairs = list(itertools.product([1, 2], ["a", "b"]))
print(len(pairs))


class DataProcessor:
    def __init__(self, data):
        self.data = data

    def filtered(self, threshold):
        return [x for x in self.data if x > threshold]

    def stats(self):
        total = sum(self.data)
        count = len(self.data)
        return {"total": total, "count": count}


proc = DataProcessor([10, 20, 30, 5, 15, 25])
print(sorted(proc.filtered(12)))
print(proc.stats()["total"])

# Try/except with custom logic
try:
    values = [1, 2, 3]
    print(values[1])
except IndexError:
    print("index error")
finally:
    print("done")

# Nested comprehension with conditional
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat_evens = [x for row in matrix for x in row if x % 2 == 0]
print(sorted(flat_evens))

# While with break
i = 0
while True:
    if i >= 3:
        break
    i = i + 1
print(f"stopped at {i}")

# F-string with expression
items = ["alpha", "beta", "gamma"]
for idx, item in enumerate(items):
    print(f"{idx}:{item}")


a = 2
if 0 <= a < 10:
    print("in range")


first, *middle, last = [1,2,3,4,5]
print(middle)


# walrus operator
if (n := len(items)) > 10:
    print(f"{n} items")


def f(x):
    return x * 2


items = list(range(20))
pairs = [(y := f(x), x) for x in items]
print(pairs)


# breaking loops
seq = range(10)

def found(x):
    return x == 20

for x in seq:
    if found(x): break
else:
    print("not found")


# force positional
def f(a, b, /, c, *, d):
    print(a + b + c + d)

f(1, 2, 3, d=4)


# slot
class P:
    __slots__ = ("x","y")
    def __init__(self,x,y):
        self.x, self.y = x,y

p = P(1, 2)
print(p.x + p.y)


# yield
def foo_yield(l):
    for i in l:
        yield i

x_foo_yield = foo_yield(list(range(100)))
print(next(x_foo_yield))
print(next(x_foo_yield))
print(next(x_foo_yield))
print(next(x_foo_yield))


# lists
a = list(range(10))
print(a[-3:])
print(a[::-1])
print(a[::2])


*a, = range(3)
print(a)


a = b = []; a.append(1); print(b)


# return format
def foo(a, b):
    return f"{a} {b}"

print(foo(1, 2))


# obfuscated

# ControlFlowFlattenObfuscator
# TODO: uncomment
# def greet(name):
#     _state=936
#     _ret=None
#     while _state!=435:
#         if _state==995:
#             msg=msg+name
#             _state=528
#         elif _state==936:
#             msg='Hello, '
#             _state=995
#         elif _state==528:
#             _ret=msg
#             _state=435
#     return _ret
#
# greet("world")
