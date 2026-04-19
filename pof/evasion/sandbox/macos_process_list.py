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

DEFAULT_PROCESS_LIST = [
    "Wireshark",
    "tcpdump",
    "dtrace",
    "lldb",
    "fsmon",
    "filemon",
    "procmon",
    "Instruments",
]


class MacProcessListEvasion(BaseEvasion):
    CATEGORY = Category.SANDBOX
    PLATFORM = Platform.DARWIN
    DESCRIPTION = "Detects known analysis tool processes on macOS"

    def __init__(self, process_list: list[str] | None = None) -> None:
        self.process_list = (
            process_list if process_list is not None else DEFAULT_PROCESS_LIST
        )

    @staticmethod
    def import_tokens() -> list[tuple[int, str]]:
        return [
            (NAME, "import"),
            (NAME, "subprocess"),
        ]

    def check_tokens(self) -> list[tuple[int, str]]:
        """Output.

        `any(x in subprocess.check_output(["ps", "-eo", "comm"]).decode()
        for x in [...])`.
        """
        proc_tokens: list[tuple[int, str]] = []
        for i, proc in enumerate(self.process_list):
            if i > 0:
                proc_tokens.append((OP, ","))
            proc_tokens.append((STRING, repr(proc)))

        return [
            (NAME, "any"),
            (LPAR, "("),
            (NAME, "x"),
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
            (NAME, "for"),
            (NAME, "x"),
            (NAME, "in"),
            (OP, "["),
            *proc_tokens,
            (OP, "]"),
            (RPAR, ")"),
        ]
