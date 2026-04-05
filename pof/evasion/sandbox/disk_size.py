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


class DiskSizeEvasion(BaseEvasion):
    CATEGORY = Category.SANDBOX
    PLATFORM = Platform.ANY
    DESCRIPTION = "Detects small disk size indicating a sandbox VM"

    def __init__(self, min_gb: int = 60) -> None:
        self.min_gb = min_gb

    @staticmethod
    def import_tokens() -> list[tuple[int, str]]:
        return [
            (NAME, "import"),
            (NAME, "shutil"),
        ]

    def check_tokens(self) -> list[tuple[int, str]]:
        """`shutil.disk_usage("/").total / (1024 ** 3) < 60`."""
        return [
            (NAME, "shutil"),
            (OP, "."),
            (NAME, "disk_usage"),
            (LPAR, "("),
            (STRING, repr("/")),
            (RPAR, ")"),
            (OP, "."),
            (NAME, "total"),
            (OP, "/"),
            (LPAR, "("),
            (NUMBER, "1024"),
            (OP, "**"),
            (NUMBER, "3"),
            (RPAR, ")"),
            (OP, "<"),
            (NUMBER, str(self.min_gb)),
        ]
