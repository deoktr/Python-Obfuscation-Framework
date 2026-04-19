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

from tokenize import LPAR, NAME, NUMBER, OP, RPAR, STRING

from pof.evasion.base import BaseEvasion, Category, Platform


class MacUptimeEvasion(BaseEvasion):
    CATEGORY = Category.SANDBOX
    PLATFORM = Platform.DARWIN
    DESCRIPTION = "Detects low uptime on macOS indicating a recently booted sandbox"

    def __init__(self, min_uptime: int = 600) -> None:
        self.min_uptime = min_uptime  # in seconds

    @staticmethod
    def import_tokens() -> list[tuple[int, str]]:
        return [
            (NAME, "import"),
            (NAME, "subprocess"),
            (OP, ","),
            (NAME, "time"),
        ]

    def check_tokens(self) -> list[tuple[int, str]]:
        """`time.time() - int(subprocess.check_output(["sysctl","-n","kern.boottime"]).decode().split("sec = ")[1].split(",")[0]) < min_uptime`."""
        return [
            (NAME, "time"),
            (OP, "."),
            (NAME, "time"),
            (LPAR, "("),
            (RPAR, ")"),
            (OP, "-"),
            (NAME, "int"),
            (LPAR, "("),
            (NAME, "subprocess"),
            (OP, "."),
            (NAME, "check_output"),
            (LPAR, "("),
            (OP, "["),
            (STRING, repr("sysctl")),
            (OP, ","),
            (STRING, repr("-n")),
            (OP, ","),
            (STRING, repr("kern.boottime")),
            (OP, "]"),
            (RPAR, ")"),
            (OP, "."),
            (NAME, "decode"),
            (LPAR, "("),
            (RPAR, ")"),
            (OP, "."),
            (NAME, "split"),
            (LPAR, "("),
            (STRING, repr("sec = ")),
            (RPAR, ")"),
            (OP, "["),
            (NUMBER, "1"),
            (OP, "]"),
            (OP, "."),
            (NAME, "split"),
            (LPAR, "("),
            (STRING, repr(",")),
            (RPAR, ")"),
            (OP, "["),
            (NUMBER, "0"),
            (OP, "]"),
            (RPAR, ")"),
            (OP, "<"),
            (NUMBER, str(self.min_uptime)),
        ]
