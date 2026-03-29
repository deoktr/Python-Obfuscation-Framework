# POF, a free and open source Python obfuscation framework.
# Copyright (C) 2022 - 2026  Deoktr
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# TODO (deoktr): obfuscate `format` but only when not after `"".`
# TODO (deoktr): add `__name__.__class__.__class__.__base__.__subclasses__()` variant

import random
from tokenize import (
    FSTRING_END,
    FSTRING_START,
    LPAR,
    LSQB,
    NAME,
    NUMBER,
    OP,
    RPAR,
    RSQB,
    STRING,
)
from typing import ClassVar

from pof.logger import logger


class BuiltinsObfuscator:
    # list(__builtins__.__dict__.keys())
    BUILTINS = (
        # "__name__",  # doesn't work with 'if _name_ == "_main_": ...'
        "__doc__",
        "__package__",
        "__loader__",
        "__spec__",
        "__build_class__",
        "__import__",
        "abs",
        "all",
        "any",
        "ascii",
        "bin",
        "breakpoint",
        "callable",
        "chr",
        "compile",
        "delattr",
        "dir",
        "divmod",
        "eval",
        "exec",
        # "format",  # try to change "{}".format('foo')
        "getattr",
        "globals",
        "hasattr",
        "hash",
        "hex",
        "id",
        "input",
        "isinstance",
        "issubclass",
        "iter",
        "aiter",
        "len",
        "locals",
        "max",
        "min",
        "next",
        "anext",
        "oct",
        "ord",
        "pow",
        "print",
        "repr",
        "round",
        "setattr",
        "sorted",
        "sum",
        "vars",
        "None",
        "Ellipsis",
        "NotImplemented",
        "False",
        "True",
        "bool",
        "memoryview",
        "bytearray",
        "bytes",
        "classmethod",
        "complex",
        "dict",
        "enumerate",
        "filter",
        "float",
        "frozenset",
        "property",
        "int",
        "list",
        "map",
        "object",
        "range",
        "reversed",
        "set",
        "slice",
        "staticmethod",
        "str",
        # "super",  # plain doesn't work
        "tuple",
        "type",
        "zip",
        "__debug__",
        "BaseException",
        "Exception",
        "TypeError",
        "StopAsyncIteration",
        "StopIteration",
        "GeneratorExit",
        "SystemExit",
        "KeyboardInterrupt",
        "ImportError",
        "ModuleNotFoundError",
        "OSError",
        "EnvironmentError",
        "IOError",
        "EOFError",
        "RuntimeError",
        "RecursionError",
        "NotImplementedError",
        "NameError",
        "UnboundLocalError",
        "AttributeError",
        "SyntaxError",
        "IndentationError",
        "TabError",
        "LookupError",
        "IndexError",
        "KeyError",
        "ValueError",
        "UnicodeError",
        "UnicodeEncodeError",
        "UnicodeDecodeError",
        "UnicodeTranslateError",
        "AssertionError",
        "ArithmeticError",
        "FloatingPointError",
        "OverflowError",
        "ZeroDivisionError",
        "SystemError",
        "ReferenceError",
        "MemoryError",
        "BufferError",
        "Warning",
        "UserWarning",
        "EncodingWarning",
        "DeprecationWarning",
        "PendingDeprecationWarning",
        "SyntaxWarning",
        "RuntimeWarning",
        "FutureWarning",
        "ImportWarning",
        "UnicodeWarning",
        "BytesWarning",
        "ResourceWarning",
        "ConnectionError",
        "BlockingIOError",
        "BrokenPipeError",
        "ChildProcessError",
        "ConnectionAbortedError",
        "ConnectionRefusedError",
        "ConnectionResetError",
        "FileExistsError",
        "FileNotFoundError",
        "IsADirectoryError",
        "NotADirectoryError",
        "InterruptedError",
        "PermissionError",
        "ProcessLookupError",
        "TimeoutError",
        "open",
        "quit",
        "exit",
        "copyright",
        "credits",
        "license",
        "help",
    )

    HARD_CODED: ClassVar[dict[list[list[tuple[int, str]]]]] = {
        "True": [
            # __name__.__eq__(__name__)
            [
                (NAME, "__name__"),
                (OP, "."),
                (NAME, "__eq__"),
                (LPAR, "("),
                (NAME, "__name__"),
                (RPAR, ")"),
            ],
            # __name__.__eq__.__call__(__name__)
            [
                (NAME, "__name__"),
                (OP, "."),
                (NAME, "__eq__"),
                (OP, "."),
                (NAME, "__call__"),
                (LPAR, "("),
                (NAME, "__name__"),
                (RPAR, ")"),
            ],
            # type(1) == type(1)
            [
                (LPAR, "("),
                (NAME, "type"),
                (LPAR, "("),
                (NUMBER, "1"),
                (RPAR, ")"),
                (OP, "=="),
                (NAME, "type"),
                (LPAR, "("),
                (NUMBER, "1"),
                (RPAR, ")"),
                (RPAR, ")"),
            ],
        ],
        "False": [
            # __name__.__ne__(__name__)
            [
                (NAME, "__name__"),
                (OP, "."),
                (NAME, "__ne__"),
                (LPAR, "("),
                (NAME, "__name__"),
                (RPAR, ")"),
            ],
            # __name__.__ne__.__call__(__name__)
            [
                (NAME, "__name__"),
                (OP, "."),
                (NAME, "__ne__"),
                (OP, "."),
                (NAME, "__call__"),
                (LPAR, "("),
                (NAME, "__name__"),
                (RPAR, ")"),
            ],
            # (type(1) != type(1))
            [
                (LPAR, "("),
                (NAME, "type"),
                (LPAR, "("),
                (NUMBER, "1"),
                (RPAR, ")"),
                (OP, "!="),
                (NAME, "type"),
                (LPAR, "("),
                (NUMBER, "1"),
                (RPAR, ")"),
                (RPAR, ")"),
            ],
            # (not bool)
            [
                (LPAR, "("),
                (NAME, "not"),
                (NAME, "bool"),
                (RPAR, ")"),
            ],
        ],
        "int": [
            # __name__.__len__().__class__
            [
                (NAME, "__name__"),
                (OP, "."),
                (NAME, "__len__"),
                (LPAR, "("),
                (RPAR, ")"),
                (OP, "."),
                (NAME, "__class__"),
            ],
            # __name__.__len__.__call__().__class__
            [
                (NAME, "__name__"),
                (OP, "."),
                (NAME, "__len__"),
                (OP, "."),
                (NAME, "__call__"),
                (LPAR, "("),
                (RPAR, ")"),
                (OP, "."),
                (NAME, "__class__"),
            ],
        ],
        "str": [
            # __name__.__class__
            [
                (NAME, "__name__"),
                (OP, "."),
                (NAME, "__class__"),
            ],
        ],
        "dict": [
            # type(__builtins__.__dict__)
            [
                (NAME, "type"),
                (LPAR, "("),
                (NAME, "__builtins__"),
                (OP, "."),
                (NAME, "__dict__"),
                (RPAR, ")"),
            ],
            # __annotations__.__class__
            [
                (NAME, "__annotations__"),
                (OP, "."),
                (NAME, "__class__"),
            ],
        ],
        "type": [
            # __name__.__class__.__class__
            [
                (NAME, "__name__"),
                (OP, "."),
                (NAME, "__class__"),
                (OP, "."),
                (NAME, "__class__"),
            ],
        ],
        "None": [
            # __name__.__class__.__base__.__base__
            [
                (NAME, "__name__"),
                (OP, "."),
                (NAME, "__class__"),
                (OP, "."),
                (NAME, "__base__"),
                (OP, "."),
                (NAME, "__base__"),
            ],
        ],
        "list": [
            # __name__.__dir__().__class__
            [
                (NAME, "__name__"),
                (OP, "."),
                (NAME, "__dir__"),
                (LPAR, "("),
                (RPAR, ")"),
                (OP, "."),
                (NAME, "__class__"),
            ],
            # __name__.__dir__.__call__().__class__
            [
                (NAME, "__name__"),
                (OP, "."),
                (NAME, "__dir__"),
                (OP, "."),
                (NAME, "__call__"),
                (LPAR, "("),
                (RPAR, ")"),
                (OP, "."),
                (NAME, "__class__"),
            ],
        ],
        "tuple": [
            # __name__.__class__.__bases__.__class__
            [
                (NAME, "__name__"),
                (OP, "."),
                (NAME, "__class__"),
                (OP, "."),
                (NAME, "__bases__"),
                (OP, "."),
                (NAME, "__class__"),
            ],
        ],
        "object": [
            # __name__.__class__.__base__
            [
                (NAME, "__name__"),
                (OP, "."),
                (NAME, "__class__"),
                (OP, "."),
                (NAME, "__base__"),
            ],
        ],
    }

    @staticmethod
    def getattribute(tokval):
        # __builtins__.__getattribute__({})
        return [
            (NAME, "__builtins__"),
            (OP, "."),
            (NAME, "__getattribute__"),
            (LPAR, "("),
            (STRING, repr(tokval)),
            (RPAR, ")"),
        ]

    @staticmethod
    def dict_getitem(tokval):
        # __builtins__.__dict__.__getitem__({})
        return [
            (NAME, "__builtins__"),
            (OP, "."),
            (NAME, "__dict__"),
            (OP, "."),
            (NAME, "__getitem__"),
            (LPAR, "("),
            (STRING, repr(tokval)),
            (RPAR, ")"),
        ]

    @staticmethod
    def dict_sqb(tokval):
        # __builtins__.__dict__[{}]
        return [
            (NAME, "__builtins__"),
            (OP, "."),
            (NAME, "__dict__"),
            (LSQB, "["),
            (STRING, repr(tokval)),
            (RSQB, "]"),
        ]

    @staticmethod
    def globals_obf(tokval):
        # TODO (deoktr): maybe obfuscate __builtins__ to `globals()['__builtins__']`
        # instead?
        # this would provide more alternative, but __builtins__ can't be
        # obfuscated like other builtins, for ex this doesn't work:
        # __builtins__.__getattribute__("__builtins__")
        # so we would have to create a special case for __builtins__
        # which is not ideal, or clean
        # but it would offer all the permutations we have for __builtins__ calls

        # globals()['__builtins__'].__dict__[{}]
        return [
            (NAME, "globals"),
            (LPAR, "("),
            (RPAR, ")"),
            (OP, "["),
            (STRING, repr("__builtins__")),
            (OP, "]"),
            (OP, "."),
            (NAME, "__dict__"),
            (LSQB, "["),
            (STRING, repr(tokval)),
            (RSQB, "]"),
        ]

    def obfuscate_builtins(self, tokval):
        # 75% to choose hard coded
        if tokval in self.HARD_CODED and random.randint(1, 4) != 1:
            return random.choice(self.HARD_CODED[tokval])

        method = random.randint(1, 4)
        if method == 1:
            return self.getattribute(tokval)
        if method == 2:  # noqa: PLR2004
            return self.dict_getitem(tokval)
        if method == 3:  # noqa: PLR2004
            return self.dict_sqb(tokval)
        if method == 4:  # noqa: PLR2004
            return self.globals_obf(tokval)

        # should never happen, but we never know
        msg = f"unsupported builtin obfuscation method {method}"
        logger.error(msg)
        return None

    def obfuscate_tokens(self, tokens):
        result = []
        parenthesis_depth = 0  # parenthesis depth
        fstring_depth = 0
        prev_tokval = None
        for index, (toknum, tokval, *_) in enumerate(tokens):
            new_tokens = [(toknum, tokval)]
            next_tokval = None
            if len(tokens) > index + 1:
                _, next_tokval, *__ = tokens[index + 1]

            if toknum == OP and tokval == "(":
                parenthesis_depth += 1
            elif toknum == OP and tokval == ")":
                parenthesis_depth -= 1

            if toknum == FSTRING_START:
                fstring_depth += 1
            elif toknum == FSTRING_END:
                fstring_depth -= 1

            if (
                toknum == NAME
                and tokval in self.BUILTINS
                and prev_tokval not in (".", "def", "class")
                and (
                    parenthesis_depth == 0
                    or (parenthesis_depth > 0 and next_tokval != "=")
                )
                and fstring_depth == 0
            ):
                new_tokens = self.obfuscate_builtins(tokval)

            if new_tokens:
                result.extend(new_tokens)
            prev_tokval = tokval
        return result
