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
from pof.evasion.utils import HOSTNAME


class SandboxHostnameEvasion(BaseEvasion):
    CATEGORY = Category.SANDBOX
    PLATFORM = Platform.ANY
    DESCRIPTION = "Detects known sandbox hostnames via socket.gethostname()"

    def __init__(self, hostnames: list[str] | None = None) -> None:
        self.hostnames = hostnames if hostnames is not None else HOSTNAME

    @staticmethod
    def import_tokens() -> list[tuple[int, str]]:
        return [
            (NAME, "import"),
            (NAME, "socket"),
        ]

    def check_tokens(self) -> list[tuple[int, str]]:
        """`socket.gethostname() in [...]`."""
        name_tokens: list[tuple[int, str]] = []
        for i, name in enumerate(self.hostnames):
            if i > 0:
                name_tokens.append((OP, ","))
            name_tokens.append((STRING, repr(name)))

        return [
            (NAME, "socket"),
            (OP, "."),
            (NAME, "gethostname"),
            (LPAR, "("),
            (RPAR, ")"),
            (NAME, "in"),
            (OP, "["),
            *name_tokens,
            (OP, "]"),
        ]
