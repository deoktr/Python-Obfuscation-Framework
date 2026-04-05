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


class VMHypervisorEvasion(BaseEvasion):
    CATEGORY = Category.SANDBOX
    PLATFORM = Platform.ANY
    DESCRIPTION = "Detects VM via MAC OUI prefix check using uuid.getnode()"

    @staticmethod
    def import_tokens() -> list[tuple[int, str]]:
        return [
            (NAME, "import"),
            (NAME, "uuid"),
        ]

    def check_tokens(self) -> list[tuple[int, str]]:
        """Output.

        `(uuid.getnode() >> 24) in [0x000C29, 0x001C14, 0x005056, 0x0003FF,
        0x00155D, 0x080027, 0x0A0027, 0x525400]`.
        """
        return [
            (LPAR, "("),
            (NAME, "uuid"),
            (OP, "."),
            (NAME, "getnode"),
            (LPAR, "("),
            (RPAR, ")"),
            (OP, ">>"),
            (NUMBER, "24"),
            (RPAR, ")"),
            (NAME, "in"),
            (OP, "["),
            (NUMBER, "0x000C29"),
            (OP, ","),
            (NUMBER, "0x001C14"),
            (OP, ","),
            (NUMBER, "0x005056"),
            (OP, ","),
            (NUMBER, "0x0003FF"),
            (OP, ","),
            (NUMBER, "0x00155D"),
            (OP, ","),
            (NUMBER, "0x080027"),
            (OP, ","),
            (NUMBER, "0x0A0027"),
            (OP, ","),
            (NUMBER, "0x525400"),
            (OP, "]"),
        ]
