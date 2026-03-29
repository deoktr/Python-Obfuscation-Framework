class Foo:
    bar = 1


print(Foo.bar)

b = getattr(Foo, "bar")
print(b)

c = Foo.__dict__["bar"]
print(c)

# TODO: enable?
# d = Foo.__dict__.get("bar")
# print(d)

# TODO: enable?
# e = Foo.__dict__.__getitem__("bar")
# print(e)

setattr(Foo, "bar", 2)
print(Foo.bar)

delattr(Foo, "bar")
try:
    print(Foo.bar)
except AttributeError:
    print("AttributeError caught")
