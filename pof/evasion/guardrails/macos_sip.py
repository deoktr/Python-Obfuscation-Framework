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


class MacSIPEvasion(BaseEvasion):
    CATEGORY = Category.GUARDRAILS
    PLATFORM = Platform.DARWIN
    DESCRIPTION = "Checks macOS System Integrity Protection (SIP) status"

    def __init__(self, expected_enabled: bool = True) -> None:
        self.expected_enabled = expected_enabled

    @staticmethod
    def import_tokens() -> list[tuple[int, str]]:
        return [
            (NAME, "import"),
            (NAME, "subprocess"),
        ]

    def check_tokens(self) -> list[tuple[int, str]]:
        """`(b"enabled" in subprocess.check_output(["csrutil", "status"])) != expected_enabled`."""
        return [
            (LPAR, "("),
            (STRING, 'b"enabled"'),
            (NAME, "in"),
            (NAME, "subprocess"),
            (OP, "."),
            (NAME, "check_output"),
            (LPAR, "("),
            (OP, "["),
            (STRING, repr("csrutil")),
            (OP, ","),
            (STRING, repr("status")),
            (OP, "]"),
            (RPAR, ")"),
            (RPAR, ")"),
            (OP, "!="),
            (NAME, "True" if self.expected_enabled else "False"),
        ]
