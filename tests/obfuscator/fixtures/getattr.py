class Foo:
    bar = 1

print(Foo.bar)

b = getattr(Foo, "bar")
print(b)

setattr(Foo, "bar", 2)
print(Foo.bar)
