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

# TODO (deoktr): make windows version
from tokenize import LPAR, NAME, NUMBER, OP, RPAR, STRING

from pof.evasion.base import BaseEvasion, Category, Platform


class LinuxRAMCountEvasion(BaseEvasion):
    CATEGORY = Category.SANDBOX
    PLATFORM = Platform.LINUX
    DESCRIPTION = "Detects low RAM indicating a sandbox VM"

    def __init__(self, min_ram: int = 2) -> None:
        """Min RAM in Gib."""
        self.min_ram = min_ram

    @staticmethod
    def import_tokens() -> list[tuple[int, str]]:
        return [
            (NAME, "import"),
            (NAME, "os"),
        ]

    def check_tokens(self) -> list[tuple[int, str]]:
        """Linux RAM count evasion tokens.

        `((os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')) / (1024.**3)) < 2`
        """
        return [
            (LPAR, "("),
            (LPAR, "("),
            (NAME, "os"),
            (OP, "."),
            (NAME, "sysconf"),
            (LPAR, "("),
            (STRING, "'SC_PAGE_SIZE'"),
            (RPAR, ")"),
            (OP, "*"),
            (NAME, "os"),
            (OP, "."),
            (NAME, "sysconf"),
            (LPAR, "("),
            (STRING, "'SC_PHYS_PAGES'"),
            (RPAR, ")"),
            (RPAR, ")"),
            (OP, "/"),
            (LPAR, "("),
            (NUMBER, "1024."),
            (OP, "**"),
            (NUMBER, "3"),
            (RPAR, ")"),
            (RPAR, ")"),
            (OP, "<"),
            (NUMBER, str(self.min_ram)),
        ]
