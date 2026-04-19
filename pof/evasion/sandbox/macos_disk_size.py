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


class MacDiskSizeEvasion(BaseEvasion):
    CATEGORY = Category.SANDBOX
    PLATFORM = Platform.DARWIN
    DESCRIPTION = "Detects small disk size on macOS indicating a sandbox VM"

    def __init__(self, min_disk: int = 50 * 1024 * 1024) -> None:
        self.min_disk = min_disk  # in KB

    @staticmethod
    def import_tokens() -> list[tuple[int, str]]:
        return [
            (NAME, "import"),
            (NAME, "subprocess"),
        ]

    def check_tokens(self) -> list[tuple[int, str]]:
        """`int(subprocess.check_output(["df","-k","/"]).decode().split("\\n")[1].split()[1]) < min_disk`."""
        return [
            (NAME, "int"),
            (LPAR, "("),
            (NAME, "subprocess"),
            (OP, "."),
            (NAME, "check_output"),
            (LPAR, "("),
            (OP, "["),
            (STRING, repr("df")),
            (OP, ","),
            (STRING, repr("-k")),
            (OP, ","),
            (STRING, repr("/")),
            (OP, "]"),
            (RPAR, ")"),
            (OP, "."),
            (NAME, "decode"),
            (LPAR, "("),
            (RPAR, ")"),
            (OP, "."),
            (NAME, "split"),
            (LPAR, "("),
            (STRING, repr("\n")),
            (RPAR, ")"),
            (OP, "["),
            (NUMBER, "1"),
            (OP, "]"),
            (OP, "."),
            (NAME, "split"),
            (LPAR, "("),
            (RPAR, ")"),
            (OP, "["),
            (NUMBER, "1"),
            (OP, "]"),
            (RPAR, ")"),
            (OP, "<"),
            (NUMBER, str(self.min_disk)),
        ]
