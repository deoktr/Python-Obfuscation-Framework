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


class LinuxScreenResolutionEvasion(BaseEvasion):
    CATEGORY = Category.SANDBOX
    PLATFORM = Platform.LINUX
    DESCRIPTION = "Detects low screen resolution in X11 indicating a headless sandbox"

    def __init__(self, min_width: int = 1024, min_height: int = 768) -> None:
        self.min_width = min_width
        self.min_height = min_height

    @staticmethod
    def import_tokens() -> list[tuple[int, str]]:
        return [
            (NAME, "import"),
            (NAME, "subprocess"),
        ]

    def check_tokens(self) -> list[tuple[int, str]]:
        """Output.

        `int(subprocess.check_output(['xrandr']).decode().split('current')[1]
        .split(',')[0].strip().split(' x ')[0]) < 1024`.
        """
        return [
            (NAME, "int"),
            (LPAR, "("),
            (NAME, "subprocess"),
            (OP, "."),
            (NAME, "check_output"),
            (LPAR, "("),
            (OP, "["),
            (STRING, repr("xrandr")),
            (OP, "]"),
            (RPAR, ")"),
            (OP, "."),
            (NAME, "decode"),
            (LPAR, "("),
            (RPAR, ")"),
            (OP, "."),
            (NAME, "split"),
            (LPAR, "("),
            (STRING, repr("current")),
            (RPAR, ")"),
            (OP, "["),
            (NUMBER, "1"),
            (OP, "]"),
            (OP, "."),
            (NAME, "split"),
            (LPAR, "("),
            (STRING, repr(",")),
            (RPAR, ")"),
            (OP, "["),
            (NUMBER, "0"),
            (OP, "]"),
            (OP, "."),
            (NAME, "strip"),
            (LPAR, "("),
            (RPAR, ")"),
            (OP, "."),
            (NAME, "split"),
            (LPAR, "("),
            (STRING, repr(" x ")),
            (RPAR, ")"),
            (OP, "["),
            (NUMBER, "0"),
            (OP, "]"),
            (RPAR, ")"),
            (OP, "<"),
            (NUMBER, str(self.min_width)),
        ]
