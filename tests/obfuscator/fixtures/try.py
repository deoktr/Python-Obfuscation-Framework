try:
    result = 10 // 0
except ZeroDivisionError:
    print("caught division error")
finally:
    print("cleanup done")
