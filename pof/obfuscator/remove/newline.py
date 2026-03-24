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

from tokenize import COMMENT, NEWLINE, NL


class NewlineObfuscator:
    """Remove empty lines."""

    @staticmethod
    def obfuscate_tokens(tokens):
        result = []  # obfuscated tokens
        prev_toknum = None
        for toknum, tokval, *_ in tokens:
            new_tokens = [(toknum, tokval)]

            # remove empty lines from the original source
            # remove empty lines created after token manipulations
            # \n after \n --> 2 new lines in a row = one is useless
            # \n after NL --> same ^
            if (toknum == NL and prev_toknum != COMMENT) or (
                toknum == NEWLINE and (prev_toknum in (NEWLINE, NL))
            ):
                new_tokens = None

            if new_tokens:
                result.extend(new_tokens)
            prev_toknum = toknum
        return result
