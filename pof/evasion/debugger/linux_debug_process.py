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


class LinuxDebugProcessEvasion(BaseEvasion):
    CATEGORY = Category.DEBUGGER
    PLATFORM = Platform.LINUX
    DESCRIPTION = "Detects debugging tools by parent process name"

    @staticmethod
    def import_tokens():
        return [
            (NAME, "import"),
            (NAME, "os"),
        ]

    @staticmethod
    def check_tokens():
        """Output.

        `any(x in open("/proc/" + str(os.getppid()) + "/comm").read() for x in
        ["pydevd", "debugpy", "pdb"])`.
        """
        return [
            (NAME, "any"),
            (LPAR, "("),
            (NAME, "x"),
            (NAME, "in"),
            (NAME, "open"),
            (LPAR, "("),
            (STRING, '"/proc/"'),
            (OP, "+"),
            (NAME, "str"),
            (LPAR, "("),
            (NAME, "os"),
            (OP, "."),
            (NAME, "getppid"),
            (LPAR, "("),
            (RPAR, ")"),
            (RPAR, ")"),
            (OP, "+"),
            (STRING, '"/comm"'),
            (RPAR, ")"),
            (OP, "."),
            (NAME, "read"),
            (LPAR, "("),
            (RPAR, ")"),
            (NAME, "for"),
            (NAME, "x"),
            (NAME, "in"),
            (OP, "["),
            (STRING, '"pydevd"'),
            (OP, ","),
            (STRING, '"debugpy"'),
            (OP, ","),
            (STRING, '"pdb"'),
            (OP, "]"),
            (RPAR, ")"),
        ]
