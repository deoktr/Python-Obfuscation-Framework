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


class WinDebugProcessEvasion(BaseEvasion):
    CATEGORY = Category.DEBUGGER
    PLATFORM = Platform.WINDOWS
    DESCRIPTION = "Detects Windows debugging tools by process name"

    @staticmethod
    def import_tokens():
        return [
            (NAME, "import"),
            (NAME, "subprocess"),
        ]

    @staticmethod
    def check_tokens():
        """Output.

        `any(x in subprocess.check_output(["tasklist"]).decode().lower()
        for x in ["x64dbg", "x32dbg", "ollydbg", "windbg", "ida",
        "immunitydebugger", "cheatengine"])`.
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
            (STRING, '"tasklist"'),
            (OP, "]"),
            (RPAR, ")"),
            (OP, "."),
            (NAME, "decode"),
            (LPAR, "("),
            (RPAR, ")"),
            (OP, "."),
            (NAME, "lower"),
            (LPAR, "("),
            (RPAR, ")"),
            (NAME, "for"),
            (NAME, "x"),
            (NAME, "in"),
            (OP, "["),
            (STRING, '"x64dbg"'),
            (OP, ","),
            (STRING, '"x32dbg"'),
            (OP, ","),
            (STRING, '"ollydbg"'),
            (OP, ","),
            (STRING, '"windbg"'),
            (OP, ","),
            (STRING, '"ida"'),
            (OP, ","),
            (STRING, '"immunitydebugger"'),
            (OP, ","),
            (STRING, '"cheatengine"'),
            (OP, "]"),
            (RPAR, ")"),
        ]
