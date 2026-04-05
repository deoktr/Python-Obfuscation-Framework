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

from tokenize import LPAR, NAME, OP, RPAR, STRING

from pof.evasion.base import BaseEvasion, Category, Platform


class LinuxMouseEvasion(BaseEvasion):
    CATEGORY = Category.SANDBOX
    PLATFORM = Platform.LINUX
    DESCRIPTION = "Detects absence of mouse input devices indicating a headless sandbox"

    @staticmethod
    def import_tokens() -> list[tuple[int, str]]:
        return [
            (NAME, "import"),
            (NAME, "os"),
        ]

    def check_tokens(self) -> list[tuple[int, str]]:
        """Output.

        `not any("mouse" in f.lower() for f in os.listdir("/dev/input/by-id/"))
        if os.path.isdir("/dev/input/by-id/") else True`.
        """
        return [
            (NAME, "not"),
            (NAME, "any"),
            (LPAR, "("),
            (STRING, repr("mouse")),
            (NAME, "in"),
            (NAME, "f"),
            (OP, "."),
            (NAME, "lower"),
            (LPAR, "("),
            (RPAR, ")"),
            (NAME, "for"),
            (NAME, "f"),
            (NAME, "in"),
            (NAME, "os"),
            (OP, "."),
            (NAME, "listdir"),
            (LPAR, "("),
            (STRING, repr("/dev/input/by-id/")),
            (RPAR, ")"),
            (RPAR, ")"),
            (NAME, "if"),
            (NAME, "os"),
            (OP, "."),
            (NAME, "path"),
            (OP, "."),
            (NAME, "isdir"),
            (LPAR, "("),
            (STRING, repr("/dev/input/by-id/")),
            (RPAR, ")"),
            (NAME, "else"),
            (NAME, "True"),
        ]
