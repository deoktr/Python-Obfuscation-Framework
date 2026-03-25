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

import ast
import random
from tokenize import NAME, NUMBER, OP, STRING

from pof.errors import PofError
from pof.logger import logger
from pof.utils.tokens import merge_implicit_strings


class CharFromDocObfuscator:
    BUILTINS = (
        "__name__",
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
        "format",
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
        "super",
        "tuple",
        "type",
        "zip",
        "__debug__",
        "BaseException",
        "BaseExceptionGroup",
        "Exception",
        "GeneratorExit",
        "KeyboardInterrupt",
        "SystemExit",
        "ArithmeticError",
        "AssertionError",
        "AttributeError",
        "BufferError",
        "EOFError",
        "ImportError",
        "LookupError",
        "MemoryError",
        "NameError",
        "OSError",
        "ReferenceError",
        "RuntimeError",
        "StopAsyncIteration",
        "StopIteration",
        "SyntaxError",
        "SystemError",
        "TypeError",
        "ValueError",
        "Warning",
        "FloatingPointError",
        "OverflowError",
        "ZeroDivisionError",
        "BytesWarning",
        "DeprecationWarning",
        "EncodingWarning",
        "FutureWarning",
        "ImportWarning",
        "PendingDeprecationWarning",
        "ResourceWarning",
        "RuntimeWarning",
        "SyntaxWarning",
        "UnicodeWarning",
        "UserWarning",
        "BlockingIOError",
        "ChildProcessError",
        "ConnectionError",
        "FileExistsError",
        "FileNotFoundError",
        "InterruptedError",
        "IsADirectoryError",
        "NotADirectoryError",
        "PermissionError",
        "ProcessLookupError",
        "TimeoutError",
        "IndentationError",
        "IndexError",
        "KeyError",
        "ModuleNotFoundError",
        "NotImplementedError",
        "RecursionError",
        "UnboundLocalError",
        "UnicodeError",
        "BrokenPipeError",
        "ConnectionAbortedError",
        "ConnectionRefusedError",
        "ConnectionResetError",
        "TabError",
        "UnicodeDecodeError",
        "UnicodeEncodeError",
        "UnicodeTranslateError",
        "ExceptionGroup",
        "EnvironmentError",
        "IOError",
        "open",
        "copyright",
        "credits",
        "license",
        "help",
    )

    @staticmethod
    def get_char_indexes(string, char):
        return [pos for pos, c in enumerate(string) if c == char]

    @classmethod
    def try_find_doc_index(cls, char):
        # take a random builtin doc and search for index in it
        builtin = random.choice(cls.BUILTINS)
        doc = __builtins__[builtin].__doc__
        if not doc:
            msg = f"doc for {builtin} is not a string"
            raise PofError(msg)
        indexes = cls.get_char_indexes(doc, char)
        if len(indexes) == 0:
            msg = "char not present"
            raise PofError(msg)
        index = random.choice(indexes)
        return builtin, index

    def obfuscate_char(self, char):
        builtin = None
        index = None
        retry = 3
        for _ in range(retry):
            try:
                builtin, index = self.try_find_doc_index(char)
            except PofError:
                pass
            else:
                break

        if builtin is None or index is None:
            msg = f"couldn't find char in doc after {retry} tries"
            raise PofError(msg)

        return [
            (NAME, builtin),
            (OP, "."),
            (NAME, "__doc__"),
            (OP, "["),
            (NUMBER, str(index)),
            (OP, "]"),
        ]

    def obfuscate_tokens(self, tokens):
        # print.__doc__[0] = 'P'
        # __builtins__.__doc__[0] = 'B'
        tokens = merge_implicit_strings(tokens)
        result = []

        for _index, (toknum, tokval, *_) in enumerate(tokens):
            new_tokens = [(toknum, tokval)]

            if toknum == STRING:
                string = ast.literal_eval(tokval)
                if len(string) == 1:
                    try:
                        new_tokens = self.obfuscate_char(string)
                    except PofError as e:
                        logger.debug(str(e))
                    except Exception:  # noqa: BLE001
                        logger.exception("Unexpected error")

            if new_tokens:
                result.extend(new_tokens)

        return result
