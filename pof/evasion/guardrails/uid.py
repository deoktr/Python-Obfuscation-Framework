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

# TODO (deoktr): add compat with windows: `ctypes.windll.shell32.IsUserAnAdmin()`
from tokenize import LPAR, NAME, NUMBER, OP, RPAR

from pof.evasion.base import BaseEvasion, Category, Platform


class LinuxUIDEvasion(BaseEvasion):
    CATEGORY = Category.GUARDRAILS
    PLATFORM = Platform.LINUX
    DESCRIPTION = "Validates target Linux UID"

    def __init__(self, uid) -> None:
        self.uid = uid

    @staticmethod
    def import_tokens():
        return [
            (NAME, "import"),
            (NAME, "os"),
        ]

    def check_tokens(self):
        """`os.getuid()!=1000`."""
        return [
            (NAME, "os"),
            (OP, "."),
            (NAME, "getuid"),
            (LPAR, "("),
            (RPAR, ")"),
            (OP, "!="),
            (NUMBER, str(self.uid)),
        ]
