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
from tokenize import FSTRING_END, FSTRING_START, NAME, OP


class CallObfuscator:
    """Add `.__call__` to call.

    ```
    print(...)
    ```

    ```
    print.__call__(...)
    ```
    """

    RESERVED_WORDS = ("type",)  # weird but if you do `type.__call__(1)` it doesn't work

    RESERVED = RESERVED_WORDS + tuple(keyword.kwlist)

    def __init__(self, frequency: float = 1.0) -> None:
        self.frequency = max(0.0, min(1.0, frequency))

    def obfuscate_tokens(self, tokens):
        result = []
        prev_tokval = None
        fstring_depth = 0
        for index, (toknum, tokval, *_) in enumerate(tokens):
            new_tokens = [(toknum, tokval)]
            next_tokval = None
            if len(tokens) > index + 1:
                _, next_tokval, *__ = tokens[index + 1]

            if toknum == FSTRING_START:
                fstring_depth += 1
            elif toknum == FSTRING_END:
                fstring_depth -= 1

            if (
                # ensure it's not a definition
                (prev_tokval is None or prev_tokval not in ["def", "class"])
                and toknum == NAME
                and tokval not in self.RESERVED
                and next_tokval == "("
                and fstring_depth == 0
                and random.random() <= self.frequency
            ):
                new_tokens.extend(
                    [
                        (OP, "."),
                        (NAME, "__call__"),
                    ],
                )

            if new_tokens:
                result.extend(new_tokens)
            prev_tokval = tokval
        return result
