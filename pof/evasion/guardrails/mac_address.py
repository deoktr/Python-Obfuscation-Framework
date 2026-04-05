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


class MACAddressEvasion(BaseEvasion):
    CATEGORY = Category.GUARDRAILS
    PLATFORM = Platform.ANY
    DESCRIPTION = "Validates target MAC address"

    def __init__(self, mac: str) -> None:
        self.mac = mac

    @staticmethod
    def import_tokens():
        return [
            (NAME, "import"),
            (NAME, "uuid"),
        ]

    def check_tokens(self):
        """`hex(uuid.getnode()) != hex(int(mac.replace(":", ""), 16))`."""
        mac_int = int(self.mac.replace(":", ""), 16)
        return [
            (NAME, "hex"),
            (LPAR, "("),
            (NAME, "uuid"),
            (OP, "."),
            (NAME, "getnode"),
            (LPAR, "("),
            (RPAR, ")"),
            (RPAR, ")"),
            (OP, "!="),
            (NAME, "hex"),
            (LPAR, "("),
            (NUMBER, repr(mac_int)),
            (RPAR, ")"),
        ]
