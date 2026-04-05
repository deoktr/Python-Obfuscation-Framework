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


class WinTmpCountEvasion(BaseEvasion):
    CATEGORY = Category.SANDBOX
    PLATFORM = Platform.WINDOWS
    DESCRIPTION = "Detects low temp file count on Windows"

    def __init__(self, tmp_count=5) -> None:
        self.tmp_count = tmp_count

    @staticmethod
    def import_tokens():
        return [
            (NAME, "import"),
            (NAME, "os"),
            (OP, ","),
            (NAME, "sys"),
        ]

    def check_tokens(self):
        r"""Check the number of files present in /tmp.

        `len(os.listdir("C:\windows\temp")) < 10`
        """
        return [
            (NAME, "len"),
            (LPAR, "("),
            (NAME, "os"),
            (OP, "."),
            (NAME, "listdir"),
            (LPAR, "("),
            (STRING, repr(r"C:\windows\temp")),
            (RPAR, ")"),
            (RPAR, ")"),
            (OP, "<"),
            (NUMBER, repr(self.tmp_count)),
        ]
