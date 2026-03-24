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

from tokenize import LPAR, NAME, NEWLINE, RPAR

from pof.utils.cipher import ShiftCipher
from pof.utils.tokens import untokenize


class ShiftObfuscator(ShiftCipher):
    """Shift cipher obfuscator."""

    def obfuscate_tokens(self, tokens):
        code = untokenize(tokens)
        return [
            (NAME, "exec"),
            (LPAR, "("),
            *self.decode_tokens(self.encode_tokens(code)),
            (RPAR, ")"),
            (NEWLINE, "\n"),
        ]
