def greet(name):
    return "Hello, " + name + "!"


def add(a, b):
    return a + b


def classify(n):
    if n > 0:
        return "positive"
    elif n == 0:
        return "zero"
    else:
        return "negative"


result = add(3, 4)
print(greet("world"))
print(result)

for i in range(3):
    print(classify(i - 1))

print("done")

var = "Hello, world"
print(var)

var = "Hello, world"
print(var)

a = len("hello")
b = int("42")
c = str(123)
d = float("3.14")
e = list(range(5))
f = tuple(range(3))
g = set(range(4))
h = dict(x=1)
i = bool(1)
j = abs(-5)
k = min(1, 2)
m = max(3, 4)
n = sum(range(5))
o = sorted(range(5))
p = reversed(range(5))
q = enumerate(range(3))
r = zip(range(3), range(3))
s = map(str, range(3))
t = filter(bool, range(3))
u = round(3.14)

print(a, b, c, d, e, f)
