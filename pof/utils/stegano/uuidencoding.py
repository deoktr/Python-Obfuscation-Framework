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

import binascii
from tokenize import NAME, NUMBER, OP, STRING


class UUIDEncoding:
    """Encode the data in a list of valid UUID.

    Idea from: https://github.com/Bl4ckM1rror/FUD-UUID-Shellcode
    """

    UUID_LEN = 32
    padding_byte = b"0"

    @classmethod
    def encode(cls, string):
        uuid_list = []

        hex_string = binascii.b2a_hex(string)

        string_chunks = [
            hex_string[i : i + cls.UUID_LEN]
            for i in range(0, len(hex_string), cls.UUID_LEN)
        ]

        for string_chunk in string_chunks:
            sc = string_chunk
            padding = cls.UUID_LEN - len(sc)
            if padding > 0:
                sc += b"1"
                sc += cls.padding_byte * (padding - 1)

            sc = sc.decode()
            uuid_chunks = [
                sc[0:8],
                sc[8:12],
                sc[12:16],
                sc[16:20],
                sc[20:],
            ]
            uuid = "-".join(uuid_chunks)

            uuid_list.append(uuid)

        if len(hex_string) % cls.UUID_LEN == 0 and len(hex_string) > 0:
            pc = (b"1" + cls.padding_byte * (cls.UUID_LEN - 1)).decode()
            uuid_chunks = [
                pc[0:8],
                pc[8:12],
                pc[12:16],
                pc[16:20],
                pc[20:],
            ]
            uuid_list.append("-".join(uuid_chunks))

        return uuid_list

    @classmethod
    def encode_tokens(cls, string):
        uuid_list = cls.encode(string)

        tokens = [(OP, "[")]
        for uuid_element in uuid_list:
            tokens.extend(((STRING, repr(uuid_element)), (OP, ",")))
        tokens.append((OP, "]"))

        return tokens

    @staticmethod
    def import_tokens():
        return [
            (NAME, "import"),
            (NAME, "binascii"),
        ]

    @classmethod
    def decode_tokens(cls, encoded_tokens):
        """UUID decode tokens.

        ```
        binascii.a2b_hex("".join(["...",]).replace("-", "").rstrip("0")[:-1])
        ```
        """
        return [
            (NAME, "binascii"),
            (OP, "."),
            (NAME, "a2b_hex"),
            (OP, "("),
            (STRING, '""'),
            (OP, "."),
            (NAME, "join"),
            (OP, "("),
            *encoded_tokens,
            (OP, ")"),
            (OP, "."),
            (NAME, "replace"),
            (OP, "("),
            (STRING, '"-"'),
            (OP, ","),
            (STRING, '""'),
            (OP, ")"),
            (OP, "."),
            (NAME, "rstrip"),
            (OP, "("),
            (STRING, repr(cls.padding_byte.decode())),
            (OP, ")"),
            (OP, "["),
            (OP, ":"),
            (OP, "-"),
            (NUMBER, "1"),
            (OP, "]"),
            (OP, ")"),
        ]
