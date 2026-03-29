transform = lambda x: x * x + 1
print(transform(3))
print(transform(4))
print(transform(5))


def foo():
    print("foo called")
    return [0, 0]


def baz():
    print("baz called")


f = lambda: 0 if 4 & -foo()[1**2**3] + 1 % 2 >> 3 and 3 != 3 ^ 2 or False else baz
f()


g = lambda x: x + 1
print(g(4))


print(f"{(lambda: 'hi')()}")
