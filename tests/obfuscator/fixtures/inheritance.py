class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return self.name + " makes a sound"


class Dog(Animal):
    def speak(self):
        return self.name + " barks"


class Cat(Animal):
    def speak(self):
        return self.name + " meows"


print(Dog("Rex").speak())
print(Cat("Whiskers").speak())


class Flyable:
    def fly(self):
        return "flying"


class Swimmable:
    def swim(self):
        return "swimming"


class Duck(Animal, Flyable, Swimmable):
    def speak(self):
        return self.name + " quacks"


d = Duck("Donald")
print(d.speak())
print(d.fly())
print(d.swim())


class Base:
    def __init__(self):
        self.parts = []

    def add(self, part):
        self.parts.append(part)


class Left(Base):
    def __init__(self):
        super().__init__()
        self.add("left")


class Right(Base):
    def __init__(self):
        super().__init__()
        self.add("right")


class Bottom(Left, Right):
    def __init__(self):
        super().__init__()
        self.add("bottom")


b = Bottom()
print(b.parts)


print([c.__name__ for c in Bottom.__mro__])


class Parent:
    def greet(self):
        return "Hello from Parent"


class Child(Parent):
    def greet(self):
        parent_msg = super().greet()
        return parent_msg + " and Child"


print(Child().greet())


print(isinstance(d, Animal))
print(isinstance(d, Flyable))
print(issubclass(Duck, Animal))
print(issubclass(Duck, Swimmable))
