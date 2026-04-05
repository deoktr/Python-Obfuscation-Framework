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

from tokenize import LPAR, NAME, NUMBER, OP, RPAR

from pof.evasion.base import BaseEvasion, Category, Platform


class WinMouseEvasion(BaseEvasion):
    CATEGORY = Category.SANDBOX
    PLATFORM = Platform.WINDOWS
    DESCRIPTION = (
        "Detects absence of mouse device on Windows indicating a headless sandbox"
    )

    @staticmethod
    def import_tokens() -> list[tuple[int, str]]:
        return [
            (NAME, "import"),
            (NAME, "ctypes"),
        ]

    def check_tokens(self) -> list[tuple[int, str]]:
        """`ctypes.windll.user32.GetSystemMetrics(19) == 0`."""
        return [
            (NAME, "ctypes"),
            (OP, "."),
            (NAME, "windll"),
            (OP, "."),
            (NAME, "user32"),
            (OP, "."),
            (NAME, "GetSystemMetrics"),
            (LPAR, "("),
            (NUMBER, "19"),
            (RPAR, ")"),
            (OP, "=="),
            (NUMBER, "0"),
        ]
