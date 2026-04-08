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

from itertools import chain
from tokenize import (
    DEDENT,
    ENCODING,
    FSTRING_START,
    INDENT,
    NAME,
    NEWLINE,
    NL,
    NUMBER,
    STRING,
    Untokenizer,
)


class NoSpaceUntokenizer(Untokenizer):
    """Custom Untokenizer that remove useless spaces after every NAME or NUMBER."""

    def compat(self, token, iterable):  # noqa: C901, PLR0912
        indents = []
        toks_append = self.tokens.append
        startline = token[0] in (NEWLINE, NL)
        prevstring = False
        prevname = False

        for tok in chain([token], iterable):
            toknum, tokval = tok[:2]
            if toknum == ENCODING:
                self.encoding = tokval
                continue

            # just a quick change to the way this part works so that spaces are
            # not added everywhere and everytimes just when it's needed
            if toknum in (NAME, NUMBER):
                if prevname:
                    tokval = " " + tokval
                prevname = True
            else:
                if prevname and toknum == FSTRING_START:
                    tokval = " " + tokval
                prevname = False

            # Insert a space between two consecutive strings
            if toknum == STRING:
                if prevstring or tokval[0] not in "'\"":
                    tokval = " " + tokval
                prevstring = True
            else:
                prevstring = False

            if toknum == INDENT:
                indents.append(tokval)
                continue
            if toknum == DEDENT:
                indents.pop()
                continue
            if toknum in (NEWLINE, NL):
                startline = True
            elif startline and indents:
                toks_append(indents[-1])
                startline = False
            toks_append(tokval)


def untokenize(iterable):
    """Custom untokenize definition to use the NoSpaceUntokenizer."""
    ut = NoSpaceUntokenizer()
    out = ut.untokenize(iterable)
    if ut.encoding is not None:
        out = out.encode(ut.encoding)
    return out


def merge_implicit_strings(tokens: list) -> list:
    """Merge implicitly concatenated string literals into a single token.

    Python allows adjacent string literals to be concatenated::

        a = ("hello"
             "world")

    The tokenizer produces separate STRING tokens for each literal.
    This function merges them so obfuscation strategies receive a single
    string value and produce valid output.
    """
    result: list = []
    i = 0
    while i < len(tokens):
        toknum = tokens[i][0]
        tokval = tokens[i][1]
        if toknum != STRING:
            result.append(tokens[i])
            i += 1
            continue

        try:
            accumulated = eval(tokval)  # noqa: S307
        except Exception:  # noqa: BLE001
            result.append(tokens[i])
            i += 1
            continue

        merged = False
        j = i + 1
        while j < len(tokens):
            next_toknum = tokens[j][0]
            if next_toknum == NL:
                j += 1
                continue
            if next_toknum == STRING:
                try:
                    next_val = eval(tokens[j][1])  # noqa: S307
                except Exception:  # noqa: BLE001
                    break
                if type(accumulated) is not type(next_val):
                    break
                accumulated += next_val
                merged = True
                j += 1
                continue
            break

        if merged:
            result.append((STRING, repr(accumulated)))
        else:
            result.append(tokens[i])
        i = j if merged else i + 1

    return result
