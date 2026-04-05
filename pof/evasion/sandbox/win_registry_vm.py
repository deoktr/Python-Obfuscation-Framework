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


class WinRegistryVMEvasion(BaseEvasion):
    CATEGORY = Category.SANDBOX
    PLATFORM = Platform.WINDOWS
    DESCRIPTION = "Detects VM indicators in Windows registry BIOS information"

    @staticmethod
    def import_tokens() -> list[tuple[int, str]]:
        return [
            (NAME, "import"),
            (NAME, "os"),
        ]

    def check_tokens(self) -> list[tuple[int, str]]:
        r"""Output.

        `any(k in os.popen("reg query HKLM\\HARDWARE\\DESCRIPTION\\System\\BIOS
        /v SystemManufacturer").read() for k in ["VirtualBox", "VMware", "QEMU",
        "Xen", "innotek"])`.
        """
        return [
            (NAME, "any"),
            (LPAR, "("),
            (NAME, "k"),
            (NAME, "in"),
            (NAME, "os"),
            (OP, "."),
            (NAME, "popen"),
            (LPAR, "("),
            (
                STRING,
                repr(
                    "reg query HKLM\\HARDWARE\\DESCRIPTION\\System\\BIOS /v SystemManufacturer",  # noqa: E501
                ),
            ),
            (RPAR, ")"),
            (OP, "."),
            (NAME, "read"),
            (LPAR, "("),
            (RPAR, ")"),
            (NAME, "for"),
            (NAME, "k"),
            (NAME, "in"),
            (OP, "["),
            (STRING, repr("VirtualBox")),
            (OP, ","),
            (STRING, repr("VMware")),
            (OP, ","),
            (STRING, repr("QEMU")),
            (OP, ","),
            (STRING, repr("Xen")),
            (OP, ","),
            (STRING, repr("innotek")),
            (OP, "]"),
            (RPAR, ")"),
        ]
