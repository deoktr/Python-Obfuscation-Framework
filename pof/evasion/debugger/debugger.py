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


class DebuggerEvasion(BaseEvasion):
    CATEGORY = Category.DEBUGGER
    PLATFORM = Platform.ANY
    DESCRIPTION = "Detects Python debugger via sys.gettrace()"

    @staticmethod
    def import_tokens():
        return [
            (NAME, "import"),
            (NAME, "sys"),
        ]

    @staticmethod
    def check_tokens():
        """Detect Python debugger.

        `hasattr(sys, 'gettrace') and sys.gettrace() is not None`
        """
        return [
            (NAME, "hasattr"),
            (LPAR, "("),
            (NAME, "sys"),
            (OP, ","),
            (STRING, "'gettrace'"),
            (RPAR, ")"),
            (NAME, "and"),
            (NAME, "sys"),
            (OP, "."),
            (NAME, "gettrace"),
            (LPAR, "("),
            (RPAR, ")"),
            (NAME, "is"),
            (NAME, "not"),
            (NAME, "None"),
        ]
