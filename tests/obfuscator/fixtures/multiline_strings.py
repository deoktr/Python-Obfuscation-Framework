# Language features: implicit string concatenation (multi-line and single-line)


# Multi-line implicit concatenation (parenthesized)
a = ("hello"
"world")
print(a)

# In function call across lines
print(("foo"
"bar"))

# Three strings across lines
b = ("one"
"two"
"three")
print(b)

# Mixed quote styles
c = ('hello'
"world")
print(c)

# Single-line implicit concatenation
d = "hello" "world"
print(d)

# Three strings on one line
e = "a" "b" "c"
print(e)
