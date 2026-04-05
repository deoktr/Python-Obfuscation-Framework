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
from pof.evasion.utils import EDR_LIST


class LinuxEDREvasion(BaseEvasion):
    CATEGORY = Category.SANDBOX
    PLATFORM = Platform.LINUX
    DESCRIPTION = "Detects EDR/security products via Linux process list"

    def __init__(self, edr_list: list[str] | None = None) -> None:
        self.edr_list = edr_list if edr_list is not None else EDR_LIST

    @staticmethod
    def import_tokens() -> list[tuple[int, str]]:
        return [
            (NAME, "import"),
            (NAME, "subprocess"),
        ]

    def check_tokens(self) -> list[tuple[int, str]]:
        """Output.

        `any(e in subprocess.check_output(["ps", "-eo", "comm"])
        .decode().lower() for e in [...])`.
        """
        edr_tokens: list[tuple[int, str]] = []
        for i, edr in enumerate(self.edr_list):
            if i > 0:
                edr_tokens.append((OP, ","))
            edr_tokens.append((STRING, repr(edr)))

        return [
            (NAME, "any"),
            (LPAR, "("),
            (NAME, "e"),
            (NAME, "in"),
            (NAME, "subprocess"),
            (OP, "."),
            (NAME, "check_output"),
            (LPAR, "("),
            (OP, "["),
            (STRING, repr("ps")),
            (OP, ","),
            (STRING, repr("-eo")),
            (OP, ","),
            (STRING, repr("comm")),
            (OP, "]"),
            (RPAR, ")"),
            (OP, "."),
            (NAME, "decode"),
            (LPAR, "("),
            (RPAR, ")"),
            (OP, "."),
            (NAME, "lower"),
            (LPAR, "("),
            (RPAR, ")"),
            (NAME, "for"),
            (NAME, "e"),
            (NAME, "in"),
            (OP, "["),
            *edr_tokens,
            (OP, "]"),
            (RPAR, ")"),
        ]


class WinEDREvasion(BaseEvasion):
    CATEGORY = Category.SANDBOX
    PLATFORM = Platform.WINDOWS
    DESCRIPTION = "Detects EDR/security products via Windows task list"

    def __init__(self, edr_list: list[str] | None = None) -> None:
        self.edr_list = edr_list if edr_list is not None else EDR_LIST

    @staticmethod
    def import_tokens() -> list[tuple[int, str]]:
        return [
            (NAME, "import"),
            (NAME, "subprocess"),
        ]

    def check_tokens(self) -> list[tuple[int, str]]:
        """Output.

        `any(e in subprocess.check_output(["tasklist"])
        .decode().lower() for e in [...])`.
        """
        edr_tokens: list[tuple[int, str]] = []
        for i, edr in enumerate(self.edr_list):
            if i > 0:
                edr_tokens.append((OP, ","))
            edr_tokens.append((STRING, repr(edr)))

        return [
            (NAME, "any"),
            (LPAR, "("),
            (NAME, "e"),
            (NAME, "in"),
            (NAME, "subprocess"),
            (OP, "."),
            (NAME, "check_output"),
            (LPAR, "("),
            (OP, "["),
            (STRING, repr("tasklist")),
            (OP, "]"),
            (RPAR, ")"),
            (OP, "."),
            (NAME, "decode"),
            (LPAR, "("),
            (RPAR, ")"),
            (OP, "."),
            (NAME, "lower"),
            (LPAR, "("),
            (RPAR, ")"),
            (NAME, "for"),
            (NAME, "e"),
            (NAME, "in"),
            (OP, "["),
            *edr_tokens,
            (OP, "]"),
            (RPAR, ")"),
        ]
