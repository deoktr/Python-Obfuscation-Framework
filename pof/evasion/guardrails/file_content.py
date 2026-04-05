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


class FileContentEvasion(BaseEvasion):
    CATEGORY = Category.GUARDRAILS
    PLATFORM = Platform.ANY
    DESCRIPTION = "Validates a file's content matches expected SHA-256 hash"

    def __init__(self, file: str, expected_hash: str) -> None:
        self.file = file
        self.expected_hash = expected_hash

    @staticmethod
    def import_tokens():
        return [
            (NAME, "import"),
            (NAME, "hashlib"),
        ]

    def check_tokens(self):
        """`hashlib.sha256(open('/path','rb').read()).hexdigest() != 'abc...'`."""
        return [
            (NAME, "hashlib"),
            (OP, "."),
            (NAME, "sha256"),
            (LPAR, "("),
            (NAME, "open"),
            (LPAR, "("),
            (STRING, repr(self.file)),
            (OP, ","),
            (STRING, repr("rb")),
            (RPAR, ")"),
            (OP, "."),
            (NAME, "read"),
            (LPAR, "("),
            (RPAR, ")"),
            (RPAR, ")"),
            (OP, "."),
            (NAME, "hexdigest"),
            (LPAR, "("),
            (RPAR, ")"),
            (OP, "!="),
            (STRING, repr(self.expected_hash)),
        ]
