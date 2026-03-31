def classify_number(n):
    match n:
        case 0:
            return "zero"
        case 1:
            return "one"
        case _:
            return "other"


print(classify_number(0))
print(classify_number(1))
print(classify_number(42))


def greet(lang):
    match lang:
        case "en":
            return "Hello"
        case "fr":
            return "Bonjour"
        case "es":
            return "Hola"
        case _:
            return "Hi"


print(greet("en"))
print(greet("fr"))
print(greet("de"))


def process_command(cmd):
    match cmd:
        case ["quit"]:
            return "quitting"
        case ["go", direction]:
            msg = "going " + direction
            return msg
        case ["pick", *items]:
            msg = "picking " + str(len(items)) + " items"
            return msg
        case _:
            return "unknown"


print(process_command(["quit"]))
print(process_command(["go", "north"]))
print(process_command(["pick", "sword", "shield"]))
print(process_command(["dance"]))


def check_value(x):
    match x:
        case n if n < 0:
            return "negative"
        case 0:
            return "zero"
        case n if n > 100:
            return "big"
        case _:
            return "normal"


print(check_value(-5))
print(check_value(0))
print(check_value(200))
print(check_value(50))


def handle_event(event):
    match event:
        case {"type": "click", "x": x, "y": y}:
            msg = "click at " + str(x) + "," + str(y)
            return msg
        case {"type": "key", "char": c}:
            msg = "key " + c
            return msg
        case _:
            return "unknown event"


print(handle_event({"type": "click", "x": 10, "y": 20}))
print(handle_event({"type": "key", "char": "a"}))
print(handle_event({"type": "scroll"}))
