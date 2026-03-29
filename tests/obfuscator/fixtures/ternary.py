x = 1 if True else 2
print(x)


def foo():
    print("foo called")


def bar():
    print("bar called")


y = 2
foo() if y > 0 and y < 10 else bar()
