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


class CPUCountEvasion(BaseEvasion):
    CATEGORY = Category.SANDBOX
    PLATFORM = Platform.ANY
    DESCRIPTION = "Detects low CPU count indicating a sandbox VM"

    def __init__(self, min_cpu_count: int = 2) -> None:
        self.min_cpu_count = min_cpu_count

    @staticmethod
    def import_tokens() -> list[tuple[int, str]]:
        return [
            (NAME, "import"),
            (NAME, "multiprocessing"),
        ]

    def check_tokens(self) -> list[tuple[int, str]]:
        """`multiprocessing.cpu_count() < 2`."""
        return [
            (NAME, "multiprocessing"),
            (OP, "."),
            (NAME, "cpu_count"),
            (LPAR, "("),
            (RPAR, ")"),
            (OP, "<"),
            (NUMBER, str(self.min_cpu_count)),
        ]
