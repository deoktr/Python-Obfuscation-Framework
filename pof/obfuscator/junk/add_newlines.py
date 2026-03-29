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

import random
from tokenize import DEDENT, INDENT, NEWLINE


class AddNewlinesObfuscator:
    """Add newlines to the code."""

    def __init__(self, frequency=0.03) -> None:
        self.frequency = frequency

    def obfuscate_tokens(self, tokens):
        result = []  # obfuscated tokens
        for index, (toknum, tokval, *_) in enumerate(tokens):
            new_tokens = [(toknum, tokval)]

            if toknum in [NEWLINE, INDENT, DEDENT]:
                if (random.randint(0, 100) / 100) <= self.frequency:
                    new_tokens.extend([(NEWLINE, "\n")])

                else:
                    next_non_indent_tokval = None
                    for i in range(index, len(tokens)):
                        tn, tv, *__ = tokens[i]
                        if tn not in [NEWLINE, INDENT, DEDENT]:
                            next_non_indent_tokval = tv
                            break

                    if next_non_indent_tokval in ["def", "class"]:
                        # add a newline before
                        new_tokens = [(NEWLINE, "\n"), *new_tokens]

            if new_tokens:
                result.extend(new_tokens)
        return result
