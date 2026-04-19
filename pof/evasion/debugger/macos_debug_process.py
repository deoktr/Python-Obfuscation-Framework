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

DEFAULT_DEBUGGERS = [
    "lldb",
    "dtrace",
    "sample",
    "spindump",
    "leaks",
]


class MacDebugProcessEvasion(BaseEvasion):
    CATEGORY = Category.DEBUGGER
    PLATFORM = Platform.DARWIN
    DESCRIPTION = "Detects macOS debugging tools by parent process name"

    def __init__(self, debuggers: list[str] | None = None) -> None:
        self.debuggers = debuggers if debuggers is not None else DEFAULT_DEBUGGERS

    @staticmethod
    def import_tokens() -> list[tuple[int, str]]:
        return [
            (NAME, "import"),
            (NAME, "subprocess"),
            (OP, ","),
            (NAME, "os"),
        ]

    def check_tokens(self) -> list[tuple[int, str]]:
        """`any(x in subprocess.check_output(["ps","-o","comm=","-p",str(os.getppid())]).decode() for x in [...])`."""
        dbg_tokens: list[tuple[int, str]] = []
        for i, dbg in enumerate(self.debuggers):
            if i > 0:
                dbg_tokens.append((OP, ","))
            dbg_tokens.append((STRING, repr(dbg)))

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
            (STRING, repr("-o")),
            (OP, ","),
            (STRING, repr("comm=")),
            (OP, ","),
            (STRING, repr("-p")),
            (OP, ","),
            (NAME, "str"),
            (LPAR, "("),
            (NAME, "os"),
            (OP, "."),
            (NAME, "getppid"),
            (LPAR, "("),
            (RPAR, ")"),
            (RPAR, ")"),
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
            *dbg_tokens,
            (OP, "]"),
            (RPAR, ")"),
        ]
