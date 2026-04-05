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

from tokenize import LPAR, NAME, NUMBER, OP, RPAR, STRING

from pof.evasion.base import BaseEvasion, Category, Platform


class LanguageLocaleEvasion(BaseEvasion):
    CATEGORY = Category.GUARDRAILS
    PLATFORM = Platform.ANY
    DESCRIPTION = "Validates target system language locale"

    def __init__(self, language: str = "en") -> None:
        self.language = language

    @staticmethod
    def import_tokens():
        return [
            (NAME, "import"),
            (NAME, "locale"),
        ]

    def check_tokens(self):
        """Check if the system language locale matches the expected value.

        `locale.getdefaultlocale()[0] is None or
        not locale.getdefaultlocale()[0].startswith(language)`
        """
        return [
            (NAME, "locale"),
            (OP, "."),
            (NAME, "getdefaultlocale"),
            (LPAR, "("),
            (RPAR, ")"),
            (OP, "["),
            (NUMBER, "0"),
            (OP, "]"),
            (NAME, "is"),
            (NAME, "None"),
            (NAME, "or"),
            (NAME, "not"),
            (NAME, "locale"),
            (OP, "."),
            (NAME, "getdefaultlocale"),
            (LPAR, "("),
            (RPAR, ")"),
            (OP, "["),
            (NUMBER, "0"),
            (OP, "]"),
            (OP, "."),
            (NAME, "startswith"),
            (LPAR, "("),
            (STRING, repr(self.language)),
            (RPAR, ")"),
        ]
