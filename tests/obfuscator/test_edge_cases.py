"""Edge-case tests migrated from legacy individual test files.

Each test preserves a unique assertion pattern not covered by
test_integration.py's parametrized round-trip tests.
"""

from __future__ import annotations

import io
from tokenize import COMMENT, generate_tokens, untokenize

from pof.obfuscator import CommentsObfuscator, ExceptionObfuscator, PrintObfuscator


_COMMENTS_SOURCE = """
'''multiline
docstring
'''

# ho
'''comment'''
import foo  # end of line comment
a=1
# comment
a+=1
class Foo:
    \"\"\"
    docstring
    \"\"\"
    m = 's'
    print("test")
    x = \"\"\"
    multiline string
    \"\"\"
if __name__ == "__main__":
    koo(a)
"""

_COMMENTS_EXPECTED = (
    "\n\n\n\n\nimport foo \na =1 \n\na +=1 \nclass Foo :\n\n"
    '    m =\'s\'\n    print ("test")\n    x ="""\n    multiline string'
    '\n    """\nif __name__ =="__main__":\n    koo (a )\n'
)


def test_comments_obfuscator_removes_all_comment_tokens():
    """Verify no COMMENT token type remains after obfuscation."""
    io_obj = io.StringIO(_COMMENTS_SOURCE)
    tokens = list(generate_tokens(io_obj.readline))
    tokens = CommentsObfuscator().obfuscate_tokens(tokens)

    for _index, (toknum, _tokval, *_) in enumerate(tokens):
        assert toknum != COMMENT, f"COMMENT token found at index {_index}"

    out = untokenize(tokens)
    assert out == _COMMENTS_EXPECTED


_PRINT_SOURCE = """
import foo
from bar import koo
a=1
print("Hello, world!")
print(a)
a+=1
print(f"{a}")
print("aa", "oo")
print(foo())
print(foo("ho", koo(), "j", 42), "e")
if __name__ == "__main__":
    koo(a)
"""

_PRINT_EXPECTED = (
    "\nimport foo \nfrom bar import koo \na =1 \n\n\na +=1 "
    '\n\n\n\n\nif __name__ =="__main__":\n    koo (a )\n'
)


def test_print_obfuscator_removes_all_print_tokens():
    """Verify no 'print' token value remains after obfuscation."""
    io_obj = io.StringIO(_PRINT_SOURCE)
    tokens = list(generate_tokens(io_obj.readline))
    tokens = PrintObfuscator().obfuscate_tokens(tokens)

    for _index, (_toknum, tokval, *_) in enumerate(tokens):
        assert tokval != "print", f"'print' token found at index {_index}"

    out = untokenize(tokens)
    assert out == _PRINT_EXPECTED


_EXCEPTION_SOURCE = """
import foo
from bar import koo
a=1
raise Exception("Hello, world!")
raise Exception(a)
a+=1
raise Exception(f"{a}")
raise OSError("aa", "oo")
raise CustomError(foo())
raise Exception(foo("ho", koo(), "j", 42), "e")
if __name__ == "__main__":
    koo(a)
"""

_EXCEPTION_EXPECTED_NO_CODES = (
    "\nimport foo \nfrom bar import koo \na =1 \nraise Exception ()\n"
    "raise Exception ()\na +=1 \nraise Exception ()\nraise OSError ()\n"
    "raise CustomError ()\nraise Exception ()\n"
    'if __name__ =="__main__":\n    koo (a )\n'
)

_EXCEPTION_EXPECTED_WITH_CODES = (
    '\nimport foo \nfrom bar import koo \na =1 \nraise Exception ("_")\n'
    'raise Exception ("_")\na +=1 \nraise Exception ("_")\nraise OSError ("_")\n'
    'raise CustomError ("_")\nraise Exception ("_")\n'
    'if __name__ =="__main__":\n    koo (a )\n'
)


def test_exception_obfuscator_default():
    """ExceptionObfuscator with default add_codes=False strips arguments."""
    io_obj = io.StringIO(_EXCEPTION_SOURCE)
    tokens = list(generate_tokens(io_obj.readline))
    tokens = ExceptionObfuscator().obfuscate_tokens(tokens)

    out = untokenize(tokens)
    assert out == _EXCEPTION_EXPECTED_NO_CODES


def test_exception_obfuscator_with_codes():
    """ExceptionObfuscator with add_codes=True and mock generator."""

    def generator():
        while True:
            yield "_"

    io_obj = io.StringIO(_EXCEPTION_SOURCE)
    tokens = list(generate_tokens(io_obj.readline))
    tokens = ExceptionObfuscator(
        add_codes=True,
        generator=generator(),
    ).obfuscate_tokens(tokens)

    out = untokenize(tokens)
    assert out == _EXCEPTION_EXPECTED_WITH_CODES
