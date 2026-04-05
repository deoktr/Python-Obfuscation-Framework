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

from tokenize import NEWLINE, OP

from pof.evasion.base import BaseEvasion
from pof.evasion.debugger.debugger import DebuggerEvasion
from pof.evasion.guardrails.expire import ExpireEvasion
from pof.evasion.sandbox.cpu_count import CPUCountEvasion
from pof.evasion.sandbox.utc import UTCEvasion


class MultiEvasion(BaseEvasion):
    def __init__(self, list_evasion=None) -> None:
        if list_evasion is None:
            list_evasion = [
                CPUCountEvasion(),
                DebuggerEvasion(),
                ExpireEvasion(),
                UTCEvasion(),
            ]
        self.list_evasion = list_evasion

    def import_tokens(self):
        tokens = []
        for evasion in self.list_evasion:
            if len(tokens) > 0:
                tokens.append((NEWLINE, "\n"))
            tokens.extend(evasion.import_tokens())
        return tokens

    def check_tokens(self):
        tokens = []
        for evasion in self.list_evasion:
            if len(tokens) > 0:
                tokens.append((OP, "or"))
            tokens.extend(
                [
                    (OP, "("),
                    *evasion.check_tokens(),
                    (OP, ")"),
                ],
            )
        return tokens
