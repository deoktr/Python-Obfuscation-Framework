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
from pof.evasion.guardrails.prompt_base import PromptBase


class WinPromptEvasion(BaseEvasion, PromptBase):
    CATEGORY = Category.GUARDRAILS
    PLATFORM = Platform.WINDOWS
    DESCRIPTION = "Prompts user for confirmation before execution (Windows)"

    @staticmethod
    def import_tokens():
        return [
            (NAME, "import"),
            (NAME, "ctypes"),
        ]

    def check_tokens(self):
        """Evasion is triggered if the message box is not pressed.

        `ctypes.windll.user32.MessageBoxW(None, message, title)`
        """
        return [
            (NAME, "not"),
            (NAME, "ctypes"),
            (OP, "."),
            (NAME, "windll"),
            (OP, "."),
            (NAME, "user32"),
            (OP, "."),
            (NAME, "MessageBoxW"),
            (LPAR, "("),
            (NAME, "None"),
            (OP, ","),
            (STRING, repr(self.message)),
            (OP, ","),
            (STRING, repr(self.title)),
            (RPAR, ")"),
        ]
