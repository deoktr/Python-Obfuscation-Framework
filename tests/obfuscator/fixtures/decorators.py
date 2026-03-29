def validate(func):
    print("validate outer")
    def wrapper(*args, **kwargs):
        print("validate")
        return func(*args, **kwargs)

    return wrapper


def validate2(func):
    print("validate2 outer")
    def wrapper(*args, **kwargs):
        print("validate2")
        return func(*args, **kwargs)

    return wrapper


@validate2
def validate3(func):
    print("validate3 outer")
    @validate
    def wrapper(*args, **kwargs):
        print("validate3")
        return func(*args, **kwargs)

    return wrapper


class DataProcessor:
    @validate
    def filtered(self):
        return "filtered"

    @validate
    @validate2
    def two_decorators(self):
        return "two_decorators"

    @validate
    @staticmethod
    @validate2
    def three_decorators():
        return "three_decorators"

    @validate3
    def foo(self):
        return "foo"

d = DataProcessor()
print(d.filtered())
print(d.two_decorators())
print(DataProcessor.three_decorators())
print(d.foo())
