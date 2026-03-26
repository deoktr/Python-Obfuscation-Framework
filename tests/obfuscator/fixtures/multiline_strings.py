# Language features: implicit string concatenation (multi-line and single-line)
a = ("hello"
"world")
print(a)

print(("foo"
"bar"))

b = ("one"
"two"
"three")
print(b)

c = ('hello'
"world")
print(c)

d = "hello" "world"
print(d)

e = "a" "b" "c"
print(e)
