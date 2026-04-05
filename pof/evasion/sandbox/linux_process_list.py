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


class LinuxProcessListEvasion(BaseEvasion):
    CATEGORY = Category.SANDBOX
    PLATFORM = Platform.LINUX
    DESCRIPTION = "Detects known analysis tool processes running on the system"

    @staticmethod
    def import_tokens() -> list[tuple[int, str]]:
        return [
            (NAME, "import"),
            (NAME, "subprocess"),
        ]

    def check_tokens(self) -> list[tuple[int, str]]:
        """Output.

        `any(x in subprocess.check_output(["ps", "-eo", "comm"]).decode()
        for x in ["wireshark", "tcpdump", "strace", "ltrace", "gdb"])`.
        """
        return [
            (NAME, "any"),
            (LPAR, "("),
            (NAME, "x"),
            (NAME, "in"),
            (NAME, "subprocess"),
            (OP, "."),
            (NAME, "check_output"),
            (LPAR, "("),
            (OP, "["),
            (STRING, repr("ps")),
            (OP, ","),
            (STRING, repr("-eo")),
            (OP, ","),
            (STRING, repr("comm")),
            (OP, "]"),
            (RPAR, ")"),
            (OP, "."),
            (NAME, "decode"),
            (LPAR, "("),
            (RPAR, ")"),
            (NAME, "for"),
            (NAME, "x"),
            (NAME, "in"),
            (OP, "["),
            (STRING, repr("wireshark")),
            (OP, ","),
            (STRING, repr("tcpdump")),
            (OP, ","),
            (STRING, repr("strace")),
            (OP, ","),
            (STRING, repr("ltrace")),
            (OP, ","),
            (STRING, repr("gdb")),
            (OP, "]"),
            (RPAR, ")"),
        ]
