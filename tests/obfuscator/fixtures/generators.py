def count_up(n):
    i = 0
    while i < n:
        yield i
        i += 1


for x in count_up(5):
    print(x)


def inner():
    yield 1
    yield 2
    yield 3


def outer():
    yield 0
    yield from inner()
    yield 4


print(list(outer()))


squares = (x * x for x in range(5))
print(list(squares))


def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


fib = fibonacci()
for _ in range(8):
    print(next(fib))


def accumulate(items):
    total = 0
    for item in items:
        total += item
        yield total


print(list(accumulate([1, 2, 3, 4, 5])))


def evens(n):
    for i in range(n):
        if i % 2 == 0:
            yield i


def doubled(gen):
    for x in gen:
        yield x * 2


print(list(doubled(evens(10))))


g = count_up(3)
print(next(g))
print(next(g))
print(next(g))
try:
    next(g)
except StopIteration:
    print("generator exhausted")
