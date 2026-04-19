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


class MacScreenResolutionEvasion(BaseEvasion):
    CATEGORY = Category.SANDBOX
    PLATFORM = Platform.DARWIN
    DESCRIPTION = "Detects low screen resolution on macOS indicating a headless sandbox"

    def __init__(self, min_width: int = 1024) -> None:
        self.min_width = min_width

    @staticmethod
    def import_tokens() -> list[tuple[int, str]]:
        return [
            (NAME, "import"),
            (NAME, "subprocess"),
        ]

    def check_tokens(self) -> list[tuple[int, str]]:
        """`int(subprocess.check_output(["osascript","-e",'tell application "Finder" to get bounds of window of desktop']).decode().split(", ")[2]) < 1024`."""
        return [
            (NAME, "int"),
            (LPAR, "("),
            (NAME, "subprocess"),
            (OP, "."),
            (NAME, "check_output"),
            (LPAR, "("),
            (OP, "["),
            (STRING, repr("osascript")),
            (OP, ","),
            (STRING, repr("-e")),
            (OP, ","),
            (
                STRING,
                repr('tell application "Finder" to get bounds of window of desktop'),
            ),
            (OP, "]"),
            (RPAR, ")"),
            (OP, "."),
            (NAME, "decode"),
            (LPAR, "("),
            (RPAR, ")"),
            (OP, "."),
            (NAME, "split"),
            (LPAR, "("),
            (STRING, repr(", ")),
            (RPAR, ")"),
            (OP, "["),
            (NUMBER, "2"),
            (OP, "]"),
            (RPAR, ")"),
            (OP, "<"),
            (NUMBER, str(self.min_width)),
        ]
