def counter():
    n = 0

    def inc():
        nonlocal n
        n += 1
        return n

    return inc


i = counter()
i()
i()
i()
print(i())
