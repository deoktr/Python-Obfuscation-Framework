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


class IPAddressEvasion(BaseEvasion):
    CATEGORY = Category.GUARDRAILS
    PLATFORM = Platform.ANY
    DESCRIPTION = "Validates target IP address or CIDR range"

    def __init__(self, ip_or_cidr: str) -> None:
        self.ip_or_cidr = ip_or_cidr

    @staticmethod
    def import_tokens():
        return [
            (NAME, "import"),
            (NAME, "socket"),
            (OP, ";"),
            (NAME, "import"),
            (NAME, "ipaddress"),
        ]

    def check_tokens(self):
        """Output.

        `not ipaddress.ip_address(socket.gethostbyname(socket.gethostname()))
        in ipaddress.ip_network(ip_or_cidr, strict=False)`.
        """
        return [
            (NAME, "not"),
            (NAME, "ipaddress"),
            (OP, "."),
            (NAME, "ip_address"),
            (LPAR, "("),
            (NAME, "socket"),
            (OP, "."),
            (NAME, "gethostbyname"),
            (LPAR, "("),
            (NAME, "socket"),
            (OP, "."),
            (NAME, "gethostname"),
            (LPAR, "("),
            (RPAR, ")"),
            (RPAR, ")"),
            (RPAR, ")"),
            (NAME, "in"),
            (NAME, "ipaddress"),
            (OP, "."),
            (NAME, "ip_network"),
            (LPAR, "("),
            (STRING, repr(self.ip_or_cidr)),
            (OP, ","),
            (NAME, "strict"),
            (OP, "="),
            (NAME, "False"),
            (RPAR, ")"),
        ]
