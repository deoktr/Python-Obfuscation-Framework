# Language features: classes, inheritance, decorators, comprehensions,
# try/except/finally, .format(), for/while loops


def log_call(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return result

    return wrapper


class Shape:
    def __init__(self, name):
        self.name = name

    def area(self):
        return 0

    def describe(self):
        return "Shape: {}, Area: {}".format(self.name, self.area())


class Rectangle(Shape):
    def __init__(self, width, height):
        super().__init__("Rectangle")
        self.width = width
        self.height = height

    @log_call
    def area(self):
        return self.width * self.height


class Circle(Shape):
    def __init__(self, radius):
        super().__init__("Circle")
        self.radius = radius

    def area(self):
        return 3 * self.radius * self.radius


shapes = [Rectangle(3, 4), Circle(5)]

# List comprehension
areas = [s.area() for s in shapes]
print(areas)

# Dict comprehension
area_map = {s.name: s.area() for s in shapes}
print(sorted(area_map.items()))

# Set comprehension
unique_types = {type(s).__name__ for s in shapes}
print(sorted(unique_types))

# String formatting
msg = "Total shapes: {}".format(len(shapes))
print(msg)

# For loop
for s in shapes:
    print("{}: {}".format(s.name, s.area()))

# While loop
count = 0
total = 0
while count < len(areas):
    total = total + areas[count]
    count = count + 1
print("Sum: {}".format(total))

# Try/except/finally
try:
    result = 10 // 0
except ZeroDivisionError:
    print("caught division error")
finally:
    print("cleanup done")
