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
from tokenize import LPAR, LSQB, NAME, NUMBER, RPAR, RSQB, STRING


class BooleanObfuscator:
    """Obfuscate booleans with multiple methods."""

    @staticmethod
    def obf_true():
        match random.randint(1, 6):
            case 1:
                # all([])
                return [
                    (NAME, "all"),
                    (LPAR, "("),
                    (LSQB, "["),
                    (RSQB, "]"),
                    (RPAR, ")"),
                ]
            case 2:
                # any([True])
                return [
                    (NAME, "any"),
                    (LPAR, "("),
                    (LSQB, "["),
                    (NAME, "True"),
                    (RSQB, "]"),
                    (RPAR, ")"),
                ]
            case 3:
                # (not False)
                return [
                    (LPAR, "("),
                    (NAME, "not"),
                    (NAME, "False"),
                    (RPAR, ")"),
                ]
            case 4:
                # (not not True)
                return [
                    (LPAR, "("),
                    (NAME, "not"),
                    (NAME, "not"),
                    (NAME, "True"),
                    (RPAR, ")"),
                ]
            case 5:
                # ("" in "")
                return [
                    (LPAR, "("),
                    (STRING, "''"),
                    (NAME, "in"),
                    (STRING, "''"),
                    (RPAR, ")"),
                ]
            case 6:
                # bool(1)
                return [
                    (NAME, "bool"),
                    (LPAR, "("),
                    (NUMBER, "1"),
                    (RPAR, ")"),
                ]

    @staticmethod
    def obf_false():
        match random.randint(1, 6):
            case 1:
                # False = all([[]])
                return [
                    (NAME, "all"),
                    (LPAR, "("),
                    (LSQB, "["),
                    (LSQB, "["),
                    (RSQB, "]"),
                    (RSQB, "]"),
                    (RPAR, ")"),
                ]
            case 2:
                # all([False])
                return [
                    (NAME, "all"),
                    (LPAR, "("),
                    (LSQB, "["),
                    (NAME, "False"),
                    (RSQB, "]"),
                    (RPAR, ")"),
                ]
            case 3:
                # (not True)
                return [
                    (LPAR, "("),
                    (NAME, "not"),
                    (NAME, "True"),
                    (RPAR, ")"),
                ]
            case 4:
                # (not not False)
                return [
                    (LPAR, "("),
                    (NAME, "not"),
                    (NAME, "not"),
                    (NAME, "False"),
                    (RPAR, ")"),
                ]
            case 5:
                # ("" not in "")
                return [
                    (LPAR, "("),
                    (STRING, "''"),
                    (NAME, "not"),
                    (NAME, "in"),
                    (STRING, "''"),
                    (RPAR, ")"),
                ]
            case 6:
                # bool(0)
                return [
                    (NAME, "bool"),
                    (LPAR, "("),
                    (NUMBER, "0"),
                    (RPAR, ")"),
                ]

    def obfuscate_boolean(self, tokval):
        if tokval == "True":
            return self.obf_true()
        return self.obf_false()

    def obfuscate_tokens(self, tokens):
        result = []
        for toknum, tokval, *_ in tokens:
            new_tokens = [(toknum, tokval)]

            if toknum == NAME and tokval in ["True", "False"]:
                new_tokens = self.obfuscate_boolean(tokval)

            if new_tokens:
                result.extend(new_tokens)
        return result
