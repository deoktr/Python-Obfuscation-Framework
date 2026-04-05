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


class FileListMissingEvasion(BaseEvasion):
    CATEGORY = Category.GUARDRAILS
    PLATFORM = Platform.ANY
    DESCRIPTION = "Validates all files in a list are absent on target"

    def __init__(self, file_list) -> None:
        self.file_list = file_list

    @staticmethod
    def import_tokens():
        return [
            (NAME, "import"),
            (NAME, "os"),
        ]

    def check_tokens(self):
        """Trigger evasion if any file from the list is present on the system.

        `any([os.path.isfile(p) for p in ['/tmp/a', '/tmp/b', ...]])`
        """
        # TODO (deoktr): change
        io_obj = io.StringIO(repr(self.file_list))
        file_list_tokens = list(generate_tokens(io_obj.readline))

        return [
            (NAME, "any"),
            (LPAR, "("),
            (OP, "["),
            (NAME, "os"),
            (OP, "."),
            (NAME, "path"),
            (OP, "."),
            (NAME, "isfile"),
            (LPAR, "("),
            (NAME, "p"),
            (RPAR, ")"),
            (NAME, "for"),
            (NAME, "p"),
            (NAME, "in"),
            *file_list_tokens,
            (OP, "]"),
            (RPAR, ")"),
        ]
