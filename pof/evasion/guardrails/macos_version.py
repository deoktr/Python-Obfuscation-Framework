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


class MacVersionEvasion(BaseEvasion):
    CATEGORY = Category.GUARDRAILS
    PLATFORM = Platform.DARWIN
    DESCRIPTION = "Checks macOS version against a minimum version"

    def __init__(self, min_version: str = "11.0") -> None:
        self.min_version = min_version

    @staticmethod
    def import_tokens() -> list[tuple[int, str]]:
        return [
            (NAME, "import"),
            (NAME, "platform"),
        ]

    def check_tokens(self) -> list[tuple[int, str]]:
        """`tuple(int(x) for x in platform.mac_ver()[0].split(".")) < tuple(int(x) for x in "11.0".split("."))`."""
        return [
            (NAME, "tuple"),
            (LPAR, "("),
            (NAME, "int"),
            (LPAR, "("),
            (NAME, "x"),
            (RPAR, ")"),
            (NAME, "for"),
            (NAME, "x"),
            (NAME, "in"),
            (NAME, "platform"),
            (OP, "."),
            (NAME, "mac_ver"),
            (LPAR, "("),
            (RPAR, ")"),
            (OP, "["),
            (NUMBER, "0"),
            (OP, "]"),
            (OP, "."),
            (NAME, "split"),
            (LPAR, "("),
            (STRING, repr(".")),
            (RPAR, ")"),
            (RPAR, ")"),
            (OP, "<"),
            (NAME, "tuple"),
            (LPAR, "("),
            (NAME, "int"),
            (LPAR, "("),
            (NAME, "x"),
            (RPAR, ")"),
            (NAME, "for"),
            (NAME, "x"),
            (NAME, "in"),
            (STRING, repr(self.min_version)),
            (OP, "."),
            (NAME, "split"),
            (LPAR, "("),
            (STRING, repr(".")),
            (RPAR, ")"),
            (RPAR, ")"),
        ]
