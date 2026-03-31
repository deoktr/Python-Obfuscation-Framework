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
import random
from tokenize import LPAR, NAME, NEWLINE, NL, OP, RPAR, STRING


class GlobalsObfuscator:
    """Change a local function/class reference.

    ```
    def aaa():
        print(...)
    aaa()
    ```

    Would become:
    ```
    def aaa():
        print(...)
    globals()['aaa']()
    ```
    """

    RESERVED = keyword.kwlist

    def __init__(self, frequency: float = 1.0) -> None:
        self.frequency = max(0.0, min(1.0, frequency))

    def obfuscate_tokens(self, tokens):
        local_functions = []
        prev_tokval = None
        prev_col = -1
        for toknum, tokval, *rest in tokens:
            start = rest[0] if rest else (0, 0)
            if prev_tokval in ["def", "class"] and toknum == NAME and prev_col == 0:
                local_functions.append(tokval)
            if toknum == NAME and tokval in ("def", "class"):
                prev_col = start[1]
            prev_tokval = tokval

        result = []
        prev_tokval = None
        in_import = False
        for index, (toknum, tokval, *_) in enumerate(tokens):
            if tokval in ("import", "from") and toknum == NAME:
                in_import = True
            elif toknum in (NEWLINE, NL):
                in_import = False

            new_tokens = [(toknum, tokval)]
            next_tokval = None
            if len(tokens) > index + 1:
                _, next_tokval, *__ = tokens[index + 1]

            if (
                tokval in local_functions
                # ensure it's not a definition
                and prev_tokval not in ["def", "class", "."]
                # ensure it's not an argument of a call
                and next_tokval != "="
                and tokval not in self.RESERVED
                # ensure it's not inside an import statement
                and not in_import
                and random.random() <= self.frequency
            ):
                new_tokens = [
                    (NAME, "globals"),
                    (LPAR, "("),
                    (RPAR, ")"),
                    (OP, "["),
                    (STRING, repr(tokval)),
                    (OP, "]"),
                ]

            if new_tokens:
                result.extend(new_tokens)
            prev_tokval = tokval
        return result
