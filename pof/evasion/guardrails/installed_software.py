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

import io
from tokenize import LPAR, NAME, OP, RPAR, generate_tokens

from pof.evasion.base import BaseEvasion, Category, Platform


class InstalledSoftwareEvasion(BaseEvasion):
    CATEGORY = Category.GUARDRAILS
    PLATFORM = Platform.ANY
    DESCRIPTION = "Validates required software is installed on target"

    def __init__(self, software: list[str]) -> None:
        self.software = software

    @staticmethod
    def import_tokens():
        return [
            (NAME, "import"),
            (NAME, "shutil"),
        ]

    def check_tokens(self):
        """`not all(shutil.which(s) is not None for s in ["python3", "git", ...])`."""
        io_obj = io.StringIO(repr(self.software))
        software_list_tokens = list(generate_tokens(io_obj.readline))

        return [
            (NAME, "not"),
            (NAME, "all"),
            (LPAR, "("),
            (NAME, "shutil"),
            (OP, "."),
            (NAME, "which"),
            (LPAR, "("),
            (NAME, "s"),
            (RPAR, ")"),
            (NAME, "is"),
            (NAME, "not"),
            (NAME, "None"),
            (NAME, "for"),
            (NAME, "s"),
            (NAME, "in"),
            *software_list_tokens,
            (RPAR, ")"),
        ]
