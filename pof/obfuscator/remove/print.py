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

# this could cause some problems, if the print statement was the
# only one present in the file
from tokenize import COMMENT, DEDENT, INDENT, NAME, NEWLINE, NL, OP


def _fill_empty_blocks(tokens):
    filled = []
    for i, (toknum, tokval, *rest) in enumerate(tokens):
        filled.append((toknum, tokval, *rest))
        if toknum == INDENT:
            j = i + 1
            while j < len(tokens) and tokens[j][0] in (NEWLINE, NL, COMMENT):
                j += 1
            if j < len(tokens) and tokens[j][0] == DEDENT:
                filled.append((NAME, "pass"))
                filled.append((NEWLINE, "\n"))
    return filled


class PrintObfuscator:
    """Remove print statements from the code."""

    @staticmethod
    def obfuscate_tokens(tokens):
        result = []  # obfuscated tokens
        parenthesis_depth = 0  # parenthesis depth
        prev_tokval = None
        print_par_depth = 0
        inside_print = False
        for toknum, tokval, *_ in tokens:
            new_tokens = [(toknum, tokval)]

            if not inside_print and toknum == NAME and tokval == "print":
                new_tokens = None
                inside_print = True
                print_par_depth = parenthesis_depth

            if inside_print:
                if print_par_depth == parenthesis_depth and (
                    tokval not in ("(", "print") and prev_tokval != "print"
                ):  # check if still inside print
                    inside_print = False
                else:
                    new_tokens = None

            if toknum == OP and tokval == "(":
                parenthesis_depth += 1
            elif toknum == OP and tokval == ")":
                parenthesis_depth -= 1

            if new_tokens:
                result.extend(new_tokens)
            prev_tokval = tokval

        # insert pass into block bodies left empty after token removal
        return _fill_empty_blocks(result)
