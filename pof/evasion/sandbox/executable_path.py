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


class ExecPathEvasion(BaseEvasion):
    CATEGORY = Category.SANDBOX
    PLATFORM = Platform.ANY
    DESCRIPTION = "Detects sandbox-related keywords in executable path"

    DEFAULT_CONTAIN_LIST = (
        "virus",
        "VIRUS",
        "sample",
        "SAMPLE",
        "sandbox",
        "SANDBOX",
        "malware",
        "Malware",
        # Anubis sandbox
        "InsideTm",
        "insidetm",
    )

    def __init__(self, contain_list=DEFAULT_CONTAIN_LIST) -> None:
        self.contain_list = contain_list

    @staticmethod
    def import_tokens():
        return [
            (NAME, "import"),
            (NAME, "pathlib"),
        ]

    def check_tokens(self):
        """Check if full exec path contains one of the specific strings.

        `any([s in str(pathlib.Path(__file__).absolute()) for s in["virus",...]])`
        """
        # TODO (deoktr): generate tokens differently
        io_obj = io.StringIO(repr(self.contain_list))
        contain_list_tokens = list(generate_tokens(io_obj.readline))

        return [
            (NAME, "any"),
            (LPAR, "("),
            (OP, "["),
            (NAME, "s"),
            (NAME, "in"),
            (NAME, "str"),
            (LPAR, "("),
            (NAME, "pathlib"),
            (OP, "."),
            (NAME, "Path"),
            (LPAR, "("),
            (NAME, "__file__"),
            (RPAR, ")"),
            (OP, "."),
            (NAME, "absolute"),
            (LPAR, "("),
            (RPAR, ")"),
            (RPAR, ")"),
            (NAME, "for"),
            (NAME, "s"),
            (NAME, "in"),
            *contain_list_tokens,
            (OP, "]"),
            (RPAR, ")"),
        ]
