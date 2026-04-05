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

# TODO (deoktr): make a version for windows
from tokenize import LPAR, NAME, NUMBER, OP, RPAR, STRING

from pof.evasion.base import BaseEvasion, Category, Platform


class LinuxProcCountEvasion(BaseEvasion):
    CATEGORY = Category.SANDBOX
    PLATFORM = Platform.LINUX
    DESCRIPTION = "Detects low process count indicating a sandbox VM"

    def __init__(self, proc_count=100) -> None:
        self.proc_count = proc_count

    @staticmethod
    def import_tokens():
        return [
            (NAME, "import"),
            (NAME, "os"),
        ]

    def check_tokens(self):
        """`len(list(filter(lambda d: d.isdigit(), os.listdir("/proc")))) < 100`."""
        return [
            (NAME, "len"),
            (LPAR, "("),
            (NAME, "list"),
            (LPAR, "("),
            (NAME, "filter"),
            (LPAR, "("),
            (NAME, "lambda"),
            (NAME, "d"),
            (OP, ":"),
            (NAME, "d"),
            (OP, "."),
            (NAME, "isdigit"),
            (LPAR, "("),
            (RPAR, ")"),
            (OP, ","),
            (NAME, "os"),
            (OP, "."),
            (NAME, "listdir"),
            (LPAR, "("),
            (STRING, repr("/proc")),
            (RPAR, ")"),
            (RPAR, ")"),
            (RPAR, ")"),
            (RPAR, ")"),
            (OP, "<"),
            (NUMBER, str(self.proc_count)),
        ]
