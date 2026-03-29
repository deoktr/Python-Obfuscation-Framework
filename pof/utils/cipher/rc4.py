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

# ruff: noqa: N802 N803 N806
import random
import string
from tokenize import DEDENT, INDENT, LPAR, NAME, NEWLINE, NUMBER, OP, RPAR, STRING

from pof.logger import logger


class RC4Cipher:
    """RC4 cipher.

    Pure Python RC4 implementation.
    Source: https://github.com/manojpandey/rc4
    """

    MOD = 256
    KEY_SIZE = 512

    def __init__(self, key=None) -> None:
        if key is None:
            la = string.ascii_letters + string.digits
            key = "".join([random.choice(la) for _ in range(self.KEY_SIZE)])
            msg = f"generated key: {key}"
            logger.info(msg)
        self.key = key

    @staticmethod
    def import_tokens():
        return [(NAME, "import"), (NAME, "codecs")]

    @classmethod
    def definition_tokens(cls):
        """RC4 decrypt function definition."""
        return [
            (NAME, "def"),
            (NAME, "rc4decrypt"),
            (OP, "("),
            (NAME, "key"),
            (OP, ","),
            (NAME, "ciphertext"),
            (OP, ")"),
            (OP, ":"),
            (NEWLINE, "\n"),
            (INDENT, "    "),
            (NAME, "def"),
            (NAME, "KSA"),
            (OP, "("),
            (NAME, "key"),
            (OP, ")"),
            (OP, ":"),
            (NEWLINE, "\n"),
            (INDENT, "        "),
            (NAME, "key_length"),
            (OP, "="),
            (NAME, "len"),
            (OP, "("),
            (NAME, "key"),
            (OP, ")"),
            (NEWLINE, "\n"),
            (NAME, "S"),
            (OP, "="),
            (NAME, "list"),
            (OP, "("),
            (NAME, "range"),
            (OP, "("),
            (NAME, str(cls.MOD)),
            (OP, ")"),
            (OP, ")"),
            (NEWLINE, "\n"),
            (NAME, "j"),
            (OP, "="),
            (NUMBER, "0"),
            (NEWLINE, "\n"),
            (NAME, "for"),
            (NAME, "i"),
            (NAME, "in"),
            (NAME, "range"),
            (OP, "("),
            (NAME, str(cls.MOD)),
            (OP, ")"),
            (OP, ":"),
            (NEWLINE, "\n"),
            (INDENT, "            "),
            (NAME, "j"),
            (OP, "="),
            (OP, "("),
            (NAME, "j"),
            (OP, "+"),
            (NAME, "S"),
            (OP, "["),
            (NAME, "i"),
            (OP, "]"),
            (OP, "+"),
            (NAME, "key"),
            (OP, "["),
            (NAME, "i"),
            (OP, "%"),
            (NAME, "key_length"),
            (OP, "]"),
            (OP, ")"),
            (OP, "%"),
            (NAME, str(cls.MOD)),
            (NEWLINE, "\n"),
            (NAME, "S"),
            (OP, "["),
            (NAME, "i"),
            (OP, "]"),
            (OP, ","),
            (NAME, "S"),
            (OP, "["),
            (NAME, "j"),
            (OP, "]"),
            (OP, "="),
            (NAME, "S"),
            (OP, "["),
            (NAME, "j"),
            (OP, "]"),
            (OP, ","),
            (NAME, "S"),
            (OP, "["),
            (NAME, "i"),
            (OP, "]"),
            (NEWLINE, "\n"),
            (DEDENT, ""),
            (NAME, "return"),
            (NAME, "S"),
            (NEWLINE, "\n"),
            (DEDENT, ""),
            (NAME, "def"),
            (NAME, "PRGA"),
            (OP, "("),
            (NAME, "S"),
            (OP, ")"),
            (OP, ":"),
            (NEWLINE, "\n"),
            (INDENT, "        "),
            (NAME, "i"),
            (OP, "="),
            (NUMBER, "0"),
            (NEWLINE, "\n"),
            (NAME, "j"),
            (OP, "="),
            (NUMBER, "0"),
            (NEWLINE, "\n"),
            (NAME, "while"),
            (NAME, "True"),
            (OP, ":"),
            (NEWLINE, "\n"),
            (INDENT, "            "),
            (NAME, "i"),
            (OP, "="),
            (OP, "("),
            (NAME, "i"),
            (OP, "+"),
            (NUMBER, "1"),
            (OP, ")"),
            (OP, "%"),
            (NAME, str(cls.MOD)),
            (NEWLINE, "\n"),
            (NAME, "j"),
            (OP, "="),
            (OP, "("),
            (NAME, "j"),
            (OP, "+"),
            (NAME, "S"),
            (OP, "["),
            (NAME, "i"),
            (OP, "]"),
            (OP, ")"),
            (OP, "%"),
            (NAME, str(cls.MOD)),
            (NEWLINE, "\n"),
            (NAME, "S"),
            (OP, "["),
            (NAME, "i"),
            (OP, "]"),
            (OP, ","),
            (NAME, "S"),
            (OP, "["),
            (NAME, "j"),
            (OP, "]"),
            (OP, "="),
            (NAME, "S"),
            (OP, "["),
            (NAME, "j"),
            (OP, "]"),
            (OP, ","),
            (NAME, "S"),
            (OP, "["),
            (NAME, "i"),
            (OP, "]"),
            (NEWLINE, "\n"),
            (NAME, "K"),
            (OP, "="),
            (NAME, "S"),
            (OP, "["),
            (OP, "("),
            (NAME, "S"),
            (OP, "["),
            (NAME, "i"),
            (OP, "]"),
            (OP, "+"),
            (NAME, "S"),
            (OP, "["),
            (NAME, "j"),
            (OP, "]"),
            (OP, ")"),
            (OP, "%"),
            (NAME, str(cls.MOD)),
            (OP, "]"),
            (NEWLINE, "\n"),
            (NAME, "yield"),
            (NAME, "K"),
            (NEWLINE, "\n"),
            (DEDENT, ""),
            (DEDENT, ""),
            (NAME, "def"),
            (NAME, "get_keystream"),
            (OP, "("),
            (NAME, "key"),
            (OP, ")"),
            (OP, ":"),
            (NEWLINE, "\n"),
            (INDENT, "        "),
            (NAME, "S"),
            (OP, "="),
            (NAME, "KSA"),
            (OP, "("),
            (NAME, "key"),
            (OP, ")"),
            (NEWLINE, "\n"),
            (NAME, "return"),
            (NAME, "PRGA"),
            (OP, "("),
            (NAME, "S"),
            (OP, ")"),
            (NEWLINE, "\n"),
            (DEDENT, ""),
            (NAME, "def"),
            (NAME, "encrypt_logic"),
            (OP, "("),
            (NAME, "key"),
            (OP, ","),
            (NAME, "text"),
            (OP, ")"),
            (OP, ":"),
            (NEWLINE, "\n"),
            (INDENT, "        "),
            (NAME, "key"),
            (OP, "="),
            (OP, "["),
            (NAME, "ord"),
            (OP, "("),
            (NAME, "c"),
            (OP, ")"),
            (NAME, "for"),
            (NAME, "c"),
            (NAME, "in"),
            (NAME, "key"),
            (OP, "]"),
            (NEWLINE, "\n"),
            (NAME, "keystream"),
            (OP, "="),
            (NAME, "get_keystream"),
            (OP, "("),
            (NAME, "key"),
            (OP, ")"),
            (NEWLINE, "\n"),
            (NAME, "res"),
            (OP, "="),
            (OP, "["),
            (OP, "]"),
            (NEWLINE, "\n"),
            (NAME, "for"),
            (NAME, "c"),
            (NAME, "in"),
            (NAME, "text"),
            (OP, ":"),
            (NEWLINE, "\n"),
            (INDENT, "            "),
            (NAME, "val"),
            (OP, "="),
            (STRING, '"%02X"'),
            (OP, "%"),
            (OP, "("),
            (NAME, "c"),
            (OP, "^"),
            (NAME, "next"),
            (OP, "("),
            (NAME, "keystream"),
            (OP, ")"),
            (OP, ")"),
            (NEWLINE, "\n"),
            (NAME, "res"),
            (OP, "."),
            (NAME, "append"),
            (OP, "("),
            (NAME, "val"),
            (OP, ")"),
            (NEWLINE, "\n"),
            (DEDENT, ""),
            (NAME, "return"),
            (STRING, '""'),
            (OP, "."),
            (NAME, "join"),
            (OP, "("),
            (NAME, "res"),
            (OP, ")"),
            (NEWLINE, "\n"),
            (DEDENT, ""),
            (NAME, "ciphertext"),
            (OP, "="),
            (NAME, "codecs"),
            (OP, "."),
            (NAME, "decode"),
            (OP, "("),
            (NAME, "ciphertext"),
            (OP, ","),
            (STRING, '"hex_codec"'),
            (OP, ")"),
            (NEWLINE, "\n"),
            (NAME, "res"),
            (OP, "="),
            (NAME, "encrypt_logic"),
            (OP, "("),
            (NAME, "key"),
            (OP, ","),
            (NAME, "ciphertext"),
            (OP, ")"),
            (NEWLINE, "\n"),
            (NAME, "return"),
            (NAME, "codecs"),
            (OP, "."),
            (NAME, "decode"),
            (OP, "("),
            (NAME, "res"),
            (OP, ","),
            (STRING, '"hex_codec"'),
            (OP, ")"),
            (OP, "."),
            (NAME, "decode"),
            (OP, "("),
            (STRING, '"utf-8"'),
            (OP, ")"),
            (NEWLINE, "\n"),
            (DEDENT, ""),
        ]

    def encode(self, string):
        if isinstance(string, bytes):
            string = string.decode()

        def KSA(key):
            key_length = len(key)
            S = list(range(self.MOD))
            j = 0
            for i in range(self.MOD):
                j = (j + S[i] + key[i % key_length]) % self.MOD
                S[i], S[j] = S[j], S[i]  # swap values
            return S

        def PRGA(S):
            i = 0
            j = 0
            while True:
                i = (i + 1) % self.MOD
                j = (j + S[i]) % self.MOD
                S[i], S[j] = S[j], S[i]
                K = S[(S[i] + S[j]) % self.MOD]
                yield K

        def get_keystream(key):
            S = KSA(key)
            return PRGA(S)

        def encrypt_logic(key, text):
            key = [ord(c) for c in key]
            keystream = get_keystream(key)
            res = []
            for c in text:
                val = "%02X" % (c ^ next(keystream))  # XOR and taking hex
                res.append(val)
            return "".join(res)

        def rc4encrypt(key, plaintext):
            plaintext = list(plaintext.encode("utf-8"))
            return encrypt_logic(key, plaintext)

        return rc4encrypt(self.key, string)

    def encode_tokens(self, string):
        return [(STRING, repr(self.encode(string)))]

    def key_tokens(self):
        return [(STRING, repr(self.key))]

    def decode_tokens(self, encoded_tokens, key_tokens=None):
        if key_tokens is None:
            key_tokens = self.key_tokens()

        return [
            (NAME, "rc4decrypt"),
            (LPAR, "("),
            *key_tokens,
            (OP, ","),
            *encoded_tokens,
            (RPAR, ")"),
        ]
