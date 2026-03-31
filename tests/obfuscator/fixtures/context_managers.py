import io


buf = io.StringIO("hello context")
with buf as f:
    print(f.read())


buf1 = io.StringIO("outer")
buf2 = io.StringIO("inner")
with buf1 as f1:
    with buf2 as f2:
        print(f1.read(), f2.read())


class MyContext:
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        print(f"entering {self.name}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"exiting {self.name}")
        return False


with MyContext("test") as ctx:
    print(f"inside {ctx.name}")


class SafeContext:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is ValueError:
            print("caught ValueError")
            return True
        return False


with SafeContext():
    raise ValueError("test error")

print("after safe context")


buf3 = io.StringIO("a")
buf4 = io.StringIO("b")
with buf3 as x, buf4 as y:
    print(x.read(), y.read())
