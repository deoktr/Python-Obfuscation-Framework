print(True)
print(False)

if True:
    print(1)

if False:
    pass
else:
    print(2)

# obfuscated
print(not False)
print(all([]))
print(any([True]))
print(not not True)
print('' in '')
print(bool(1))
print(bool(1&1))
print(bool(~0))

print(bool(1&0))
print(bool(1^1))
print(bool(0|0))
