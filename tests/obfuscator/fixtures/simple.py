# Language features: functions, string concatenation, arithmetic,
# conditionals, for loop, print statements


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
