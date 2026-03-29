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
