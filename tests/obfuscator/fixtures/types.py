from typing import Optional, List, Dict, Final, Literal, Annotated

a: int = 42
b: float = 4.2
c: str = "42"
d: bool = True

print(a)
print(b)
print(c)
print(d)


def foo(x: int, y: float) -> float:
    return x + y


print(foo(1, 1.1))
print(foo(2, 2.2))


class Foo:
    def __init__(self, foo1: str = "foo", foo2: int = 1, foo3: str | None = None):
        self.foo1 = foo1
        self.foo2 = foo2
        self.foo3 = foo3

    def print(self):
        print(self.foo1)
        print(self.foo2)
        print(self.foo3)


Foo().print()


def foo_opt(a: Optional[int]) -> Optional[int]:
    if a is None:
        return None
    return a * 2


print(foo_opt(None))
print(foo_opt(1))


PI: Final = 3.1415
Mode = Literal["r", "w"]
Score = Annotated[int, "0-100"]
