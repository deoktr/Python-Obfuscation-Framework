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


class WinRAMCountEvasion(BaseEvasion):
    CATEGORY = Category.SANDBOX
    PLATFORM = Platform.WINDOWS
    DESCRIPTION = "Detects low RAM on Windows indicating a sandbox VM"

    def __init__(self, min_ram: int = 2) -> None:
        """Min RAM in GiB."""
        self.min_ram = min_ram

    @staticmethod
    def import_tokens() -> list[tuple[int, str]]:
        return [
            (NAME, "import"),
            (NAME, "os"),
        ]

    def check_tokens(self) -> list[tuple[int, str]]:
        """Output.

        `int(os.popen("wmic ComputerSystem get TotalPhysicalMemory").read()
            .split()[-1]) // (1024 ** 3) < min_ram`.
        """
        return [
            (NAME, "int"),
            (LPAR, "("),
            (NAME, "os"),
            (OP, "."),
            (NAME, "popen"),
            (LPAR, "("),
            (STRING, repr("wmic ComputerSystem get TotalPhysicalMemory")),
            (RPAR, ")"),
            (OP, "."),
            (NAME, "read"),
            (LPAR, "("),
            (RPAR, ")"),
            (OP, "."),
            (NAME, "split"),
            (LPAR, "("),
            (RPAR, ")"),
            (OP, "["),
            (OP, "-"),
            (NUMBER, "1"),
            (OP, "]"),
            (RPAR, ")"),
            (OP, "//"),
            (LPAR, "("),
            (NUMBER, "1024"),
            (OP, "**"),
            (NUMBER, "3"),
            (RPAR, ")"),
            (OP, "<"),
            (NUMBER, str(self.min_ram)),
        ]
