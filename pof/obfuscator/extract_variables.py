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

import keyword
from tokenize import DEDENT, ENCODING, INDENT, NAME, NEWLINE, NL, NUMBER, OP, STRING

from pof.utils.generator import BasicGenerator


class ExtractVariablesObfuscator:
    """Obfuscate by adding variables."""

    # BUILTINS = list(__builtins__.__dict__.keys())
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

    RESERVED_WORDS = (
        "__init__",
        "__eq__",
        "__lt__",
        "append",  # on list
        "update",  # on dict
        "copy",  # copy dict or list
        "join",  # on string "".join()
        # TODO (deoktr): add all the others
    )

    RESERVED = RESERVED_WORDS + BUILTINS + tuple(keyword.kwlist)
    KEYWORDS = tuple(keyword.kwlist)

    CONTINUATION_KEYWORDS = ("elif", "else", "except", "finally")

    def __init__(self, generator=None) -> None:
        if generator is None:
            generator = BasicGenerator.alphabet_generator()
        self.generator = generator

    def generate_new_name(self):
        return next(self.generator)

    def obfuscate_tokens(self, tokens):  # noqa: C901
        result = []
        new_line_buffer = []
        line_buffer = []
        parenthesis_depth = 0
        prev_toknum = None
        in_decorator = False

        for toknum, tokval, *_ in tokens:
            new_tokens = [(toknum, tokval)]

            if toknum == OP and tokval == "(":
                parenthesis_depth += 1
            elif toknum == OP and tokval == ")":
                parenthesis_depth -= 1

            # track decorator context, suppress flushing between @ and def/class
            if toknum == OP and tokval == "@":
                in_decorator = True
            elif in_decorator and toknum == NAME and tokval in ("def", "class"):
                in_decorator = False

            is_docstring = toknum == STRING and (
                prev_toknum in [NEWLINE, DEDENT, INDENT, ENCODING]
            )

            # check if current line starts with a continuation keyword if so,
            # skip extraction to avoid scope issues
            first_name_in_line = None
            for tok in line_buffer:
                if tok[0] == NAME:
                    first_name_in_line = tok[1]
                    break
            on_continuation_line = first_name_in_line in self.CONTINUATION_KEYWORDS

            if (
                (toknum == STRING and not is_docstring) or toknum == NUMBER
            ) and not on_continuation_line:
                random_name = self.generate_new_name()
                new_line_buffer.extend(
                    [
                        (NEWLINE, "\n"),
                        (NAME, random_name),
                        (OP, "="),
                        *new_tokens,
                    ],
                )
                new_tokens = [(NAME, random_name)]

            is_newline = toknum in (NEWLINE, NL) and tokval == "\n"
            can_flush = is_newline and parenthesis_depth == 0 and not in_decorator

            if can_flush:
                new_tokens = new_line_buffer + new_tokens + line_buffer
                new_line_buffer = []
                line_buffer = []
            elif toknum in (INDENT, DEDENT):
                new_line_buffer.extend(new_tokens)
                new_tokens = None
            else:
                line_buffer.extend(new_tokens)
                new_tokens = None

            if new_tokens:
                result.extend(new_tokens)
            prev_toknum = toknum
        return result
