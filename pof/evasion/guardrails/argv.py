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

from tokenize import NAME, NUMBER, OP, STRING

from pof.evasion.base import BaseEvasion, Category, Platform


class ArgvEvasion(BaseEvasion):
    CATEGORY = Category.GUARDRAILS
    PLATFORM = Platform.ANY
    DESCRIPTION = "Validates specific command-line arguments are passed"

    def __init__(self, argv=None) -> None:
        if argv is None:
            argv = []
        self.argv = argv

    @staticmethod
    def import_tokens():
        return [
            (NAME, "import"),
            (NAME, "sys"),
        ]

    def check_tokens(self):
        """Argument check tokens.

        `len(sys.argv)<=1 or not all(a in sys.argv[:1] for a in ["123"])`
        """
        list_args = [(OP, "[")]
        for arg in self.argv:
            list_args.extend(
                [
                    (STRING, repr(arg)),
                    (OP, ","),
                ],
            )
        list_args.append((OP, "]"))

        return [
            (NAME, "len"),
            (OP, "("),
            (NAME, "sys"),
            (OP, "."),
            (NAME, "argv"),
            (OP, ")"),
            (OP, "<="),
            (NUMBER, "1"),
            (NAME, "or"),
            (NAME, "not"),
            (NAME, "all"),
            (OP, "("),
            (NAME, "a"),
            (NAME, "in"),
            (NAME, "sys"),
            (OP, "."),
            (NAME, "argv"),
            (OP, "["),
            (NUMBER, "1"),
            (OP, ":"),
            (OP, "]"),
            (NAME, "for"),
            (NAME, "a"),
            (NAME, "in"),
            *list_args,
            (OP, ")"),
        ]
