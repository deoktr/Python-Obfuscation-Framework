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

from tokenize import LPAR, NAME, OP, RPAR

from pof.evasion.base import BaseEvasion, Category, Platform


class WinDebuggerEvasion(BaseEvasion):
    CATEGORY = Category.GUARDRAILS
    PLATFORM = Platform.WINDOWS
    DESCRIPTION = "Detects attached debugger on Windows via IsDebuggerPresent"

    @staticmethod
    def import_tokens():
        return [
            (NAME, "import"),
            (NAME, "ctypes"),
        ]

    @staticmethod
    def check_tokens():
        """`ctypes.windll.kernel32.IsDebuggerPresent()`."""
        return [
            (NAME, "ctypes"),
            (OP, "."),
            (NAME, "windll"),
            (OP, "."),
            (NAME, "kernel32"),
            (OP, "."),
            (NAME, "IsDebuggerPresent"),
            (LPAR, "("),
            (RPAR, ")"),
        ]
