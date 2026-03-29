print("Hello, world!")

msg = "Hello, {}".format("world!")
print(msg)

# format
print(f"{3}")

a = 42
print(f"{a}")

print("%s".format("Hello"))

print(f"{(n:=len([1,2,3]))=}")

# multi-line strings/split strings
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

# obfuscated

# Reverse
print('dlrow ,olleH'[::-1])

# Replace
print('Helnelemd'.replace('nelem','lo, worl'))

# One on n
print("".join([d if g%3==0 else""for g,d in enumerate('H9IesYlvJl5loU4,dK nDw51ovsrozl0UdoI!jL')]))

# Hex-encoded
print('\x48\x65\x6c\x6c\x6f\x2c\x20\x77\x6f\x72\x6c\x64')

# Unicode
print('\u0048\u0065\u006c\u006c\u006f\u002c\u0020\u0077\u006f\u0072\u006c\u0064')

# Shift cipher
print("".join([chr(ord(i)-3)for i in'Khoor/#zruog']))

# Base 64 encoding
from base64 import b64decode
print(b64decode( b'SGVsbG8sIHdvcmxk').decode())

# Base 85
from base64 import b85decode
print(b85decode( b'NM&qnZ!92pZ*pv8').decode())
