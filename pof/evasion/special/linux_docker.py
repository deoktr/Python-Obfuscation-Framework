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


class LinuxDockerEvasion(BaseEvasion):
    CATEGORY = Category.SPECIAL
    PLATFORM = Platform.LINUX
    DESCRIPTION = "Detects Docker container execution"

    @staticmethod
    def import_tokens():
        return [
            (NAME, "import"),
            (NAME, "os"),
        ]

    @staticmethod
    def check_tokens():
        """Output.

        `os.path.exists("/.dockerenv") or (os.path.exists("/proc/1/cgroup")
        and "docker" in open("/proc/1/cgroup").read())`.
        """
        return [
            (NAME, "os"),
            (OP, "."),
            (NAME, "path"),
            (OP, "."),
            (NAME, "exists"),
            (LPAR, "("),
            (STRING, '"/.dockerenv"'),
            (RPAR, ")"),
            (NAME, "or"),
            (LPAR, "("),
            (NAME, "os"),
            (OP, "."),
            (NAME, "path"),
            (OP, "."),
            (NAME, "exists"),
            (LPAR, "("),
            (STRING, '"/proc/1/cgroup"'),
            (RPAR, ")"),
            (NAME, "and"),
            (STRING, '"docker"'),
            (NAME, "in"),
            (NAME, "open"),
            (LPAR, "("),
            (STRING, '"/proc/1/cgroup"'),
            (RPAR, ")"),
            (OP, "."),
            (NAME, "read"),
            (LPAR, "("),
            (RPAR, ")"),
            (RPAR, ")"),
        ]
