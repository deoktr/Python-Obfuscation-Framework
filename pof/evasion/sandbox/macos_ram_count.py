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


class MacRAMCountEvasion(BaseEvasion):
    CATEGORY = Category.SANDBOX
    PLATFORM = Platform.DARWIN
    DESCRIPTION = "Detects low RAM on macOS indicating a sandbox VM"

    def __init__(self, min_ram: int = 2 * 1024 * 1024 * 1024) -> None:
        self.min_ram = min_ram

    @staticmethod
    def import_tokens() -> list[tuple[int, str]]:
        return [
            (NAME, "import"),
            (NAME, "subprocess"),
        ]

    def check_tokens(self) -> list[tuple[int, str]]:
        """Output.

        `int(subprocess.check_output(["sysctl", "-n", "hw.memsize"]).strip()) <
        min_ram`.
        """
        return [
            (NAME, "int"),
            (LPAR, "("),
            (NAME, "subprocess"),
            (OP, "."),
            (NAME, "check_output"),
            (LPAR, "("),
            (OP, "["),
            (STRING, repr("sysctl")),
            (OP, ","),
            (STRING, repr("-n")),
            (OP, ","),
            (STRING, repr("hw.memsize")),
            (OP, "]"),
            (RPAR, ")"),
            (OP, "."),
            (NAME, "strip"),
            (LPAR, "("),
            (RPAR, ")"),
            (RPAR, ")"),
            (OP, "<"),
            (NUMBER, str(self.min_ram)),
        ]
