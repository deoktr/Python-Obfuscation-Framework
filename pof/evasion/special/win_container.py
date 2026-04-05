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


class WinContainerEvasion(BaseEvasion):
    CATEGORY = Category.SPECIAL
    PLATFORM = Platform.WINDOWS
    DESCRIPTION = "Detects Windows container execution"

    @staticmethod
    def import_tokens():
        return [
            (NAME, "import"),
            (NAME, "os"),
        ]

    @staticmethod
    def check_tokens():
        r"""Output.

        `os.environ.get("CONTAINER", "") != "" or
        os.path.exists("C:\ServiceProfiles")`.
        """
        return [
            (NAME, "os"),
            (OP, "."),
            (NAME, "environ"),
            (OP, "."),
            (NAME, "get"),
            (LPAR, "("),
            (STRING, '"CONTAINER"'),
            (OP, ","),
            (STRING, '""'),
            (RPAR, ")"),
            (OP, "!="),
            (STRING, '""'),
            (NAME, "or"),
            (NAME, "os"),
            (OP, "."),
            (NAME, "path"),
            (OP, "."),
            (NAME, "exists"),
            (LPAR, "("),
            (STRING, '"C:\\\\ServiceProfiles"'),
            (RPAR, ")"),
        ]
