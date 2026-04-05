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

# TODO (deoktr): windows version: https://www.geeksforgeeks.org/getting-the-time-since-os-startup-using-python/
from tokenize import LPAR, NAME, NUMBER, OP, RPAR, STRING

from pof.evasion.base import BaseEvasion, Category, Platform


class LinuxUptimeEvasion(BaseEvasion):
    CATEGORY = Category.SANDBOX
    PLATFORM = Platform.LINUX
    DESCRIPTION = "Detects low system uptime indicating a fresh VM"

    def __init__(self, uptime=12 * 60) -> None:
        # uptime is in seconds
        # default: 12 minutes
        self.uptime = uptime

    @staticmethod
    def import_tokens():
        return [
            (NAME, "from"),
            (NAME, "pathlib"),
            (NAME, "import"),
            (NAME, "Path"),
        ]

    def check_tokens(self):
        """Validates system uptime i sufficient.

        `float(Path("/proc/uptime").read_text().split()[0]) < 12**60`
        """
        return [
            (NAME, "float"),
            (LPAR, "("),
            (NAME, "Path"),
            (LPAR, "("),
            (STRING, repr("/proc/uptime")),
            (RPAR, ")"),
            (OP, "."),
            (NAME, "read_text"),
            (LPAR, "("),
            (RPAR, ")"),
            (OP, "."),
            (NAME, "split"),
            (LPAR, "("),
            (RPAR, ")"),
            (OP, "["),
            (NUMBER, "0"),
            (OP, "]"),
            (RPAR, ")"),
            (OP, "<"),
            (NUMBER, str(self.uptime)),
        ]
