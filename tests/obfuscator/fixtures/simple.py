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
