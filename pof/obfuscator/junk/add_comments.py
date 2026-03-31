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

# TODO (deoktr): calculate frequency based on the number of lines to distribute
# the comment evenly across the code
import random
from tokenize import COMMENT, DEDENT, INDENT, NEWLINE

from pof.utils.generator import CommentGenerator


class AddCommentsObfuscator:
    """Add comments to the code."""

    def __init__(
        self,
        frequency=0.03,
        generator=None,
    ) -> None:
        self.frequency = max(0.0, min(1.0, frequency))

        if generator is None:
            generator = CommentGenerator.realistic_generator()

        self.generator = generator

    def get_comment(self):
        return next(self.generator)

    def obfuscate_tokens(self, tokens):
        result = []  # obfuscated tokens
        for toknum, tokval, *_ in tokens:
            new_tokens = [(toknum, tokval)]

            if (
                toknum in [NEWLINE, INDENT, DEDENT]
                and (random.randint(0, 100) / 100) <= self.frequency
            ):
                c = self.get_comment()
                if c is not None:
                    new_tokens.extend([(COMMENT, c), (NEWLINE, "\n")])

            if new_tokens:
                result.extend(new_tokens)
        return result
