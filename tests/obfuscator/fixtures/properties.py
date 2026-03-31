class Temperature:
    def __init__(self, celsius):
        self._celsius = celsius

    @property
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("Below absolute zero")
        self._celsius = value

    @property
    def fahrenheit(self):
        return self._celsius * 9 / 5 + 32


t = Temperature(100)
print(t.celsius)
print(t.fahrenheit)
t.celsius = 0
print(t.celsius)
print(t.fahrenheit)


class Circle:
    def __init__(self, radius):
        self._radius = radius

    @property
    def radius(self):
        return self._radius

    @property
    def area(self):
        return 3.14159 * self._radius ** 2


c = Circle(5)
print(c.radius)
print(round(c.area, 2))


class Counter:
    _count = 0

    def __init__(self):
        Counter._count += 1

    @classmethod
    def get_count(cls):
        return cls._count

    @staticmethod
    def description():
        return "A simple counter"


a = Counter()
b = Counter()
c = Counter()
print(Counter.get_count())
print(Counter.description())


class Name:
    def __init__(self, first, last):
        self.first = first
        self.last = last

    @property
    def full(self):
        return self.first + " " + self.last


n = Name("John", "Doe")
print(n.full)
n.first = "Jane"
print(n.full)
