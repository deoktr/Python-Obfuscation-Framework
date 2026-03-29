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

# TODO (deoktr): work with f"" strings, r"" strings etc.
# TODO (deoktr): can't split `\` !!!
# TODO (deoktr): add variable to import or not b64decode
# TODO (deoktr): replace eval with ast.literal_eval: https://beta.ruff.rs/docs/rules/suspicious-eval-usage/

import random
from base64 import b64encode, b85encode
from enum import Enum
from tokenize import (
    DEDENT,
    ENCODING,
    INDENT,
    LPAR,
    NAME,
    NEWLINE,
    NUMBER,
    OP,
    RPAR,
    STRING,
)

from pof.errors import PofError
from pof.logger import logger
from pof.utils.cipher import ShiftCipher
from pof.utils.generator import AdvancedGenerator
from pof.utils.tokens import merge_implicit_strings


class StringsObfuscator:
    """Obfuscate strings."""

    class Strats(Enum):
        BASE64 = 1
        ADDITION = 2
        ONLY_ADDITION = 3
        BASE85 = 4
        HEX = 5
        UNICODE = 6
        SHIFT = 7
        REPLACE = 8
        REVERSE = 9
        ONE_ON_N = 10

    ALL = (
        Strats.BASE64,
        Strats.BASE85,
        Strats.SHIFT,
        Strats.REPLACE,
        Strats.REVERSE,
    )

    def __init__(
        self,
        shift_cipher_class_obj=None,
        b64decode_name: str = "b64decode",
        b85decode_name: str = "b85decode",
        *,
        import_b64decode: bool = True,
        import_b85decode: bool = True,
    ) -> None:
        self.import_b64decode = import_b64decode
        self.import_b85decode = import_b85decode

        self.b64decode_name = b64decode_name
        self.b85decode_name = b85decode_name

        if shift_cipher_class_obj is None:
            shift_cipher_class_obj = ShiftCipher()
        self.shift_cipher_class_obj = shift_cipher_class_obj

    @staticmethod
    def _is_bytes_literal(tokval: str) -> bool:
        """Check if a string token represents a bytes literal (b'...' or B'...')."""
        prefix = tokval.split("'", maxsplit=1)[0].split('"')[0]
        return "b" in prefix or "B" in prefix

    def _obf_shift(self, tokval: str):
        # TODO (deoktr): choose random padding here
        raw_string = eval(tokval)  # noqa: S307
        if isinstance(raw_string, bytes):
            try:
                raw_string = raw_string.decode()
            except UnicodeDecodeError:
                return [(STRING, tokval)]
        if not raw_string.isascii():
            return [(STRING, tokval)]
        encoded = self.shift_cipher_class_obj.encode_tokens(raw_string)
        return self.shift_cipher_class_obj.decode_tokens(encoded)

    def _obf_base64(self, tokval: str):
        """Obfuscate string with base64.

        ```
        b64decode(b'...').decode()
        ```
        """
        raw_string = eval(tokval)  # noqa: S307
        is_bytes = isinstance(raw_string, bytes)
        if isinstance(raw_string, str):
            raw_string = raw_string.encode()
        b64encoded_string = b64encode(raw_string).decode()
        tokens = [
            (NAME, self.b64decode_name),
            (LPAR, "("),
            (STRING, repr(b64encoded_string)),
            (RPAR, ")"),
        ]
        if not is_bytes:
            tokens.extend(
                [
                    (OP, "."),
                    (NAME, "decode"),
                    (LPAR, "("),
                    (RPAR, ")"),
                ],
            )
        return tokens

    def _obf_base85(self, tokval: str):
        """Obfuscate string with base85.

        ```
        b85decode(b'...').decode()
        ```
        """
        raw_string = eval(tokval)  # noqa: S307
        is_bytes = isinstance(raw_string, bytes)
        if isinstance(raw_string, str):
            raw_string = raw_string.encode()
        b85encoded_string = b85encode(raw_string).decode()
        tokens = [
            (NAME, self.b85decode_name),
            (LPAR, "("),
            (STRING, repr(b85encoded_string)),
            (RPAR, ")"),
        ]
        if not is_bytes:
            tokens.extend(
                [
                    (OP, "."),
                    (NAME, "decode"),
                    (LPAR, "("),
                    (RPAR, ")"),
                ],
            )
        return tokens

    @staticmethod
    def _hex(tokval: str):
        # Hello --> \x48\x65\x6c\x6c\x6f
        raw_string = eval(tokval)  # noqa: S307
        if isinstance(raw_string, bytes):
            encoded = "".join(f"\\x{b:02x}" for b in raw_string)
            return [(STRING, f"b'{encoded}'")]
        encoded = ""
        for c in raw_string:
            code = ord(c)
            if c.isdigit():
                encoded += c
            elif code <= 0xFF:  # noqa: PLR2004
                encoded += f"\\x{code:02x}"
            elif code <= 0xFFFF:  # noqa: PLR2004
                encoded += f"\\u{code:04x}"
            else:
                encoded += f"\\U{code:08x}"
        return [(STRING, f"'{encoded}'")]

    @staticmethod
    def _unicode(tokval: str):
        # Hell --> \u0048\u0065\u006C\u006C
        raw_string = eval(tokval)  # noqa: S307
        if isinstance(raw_string, bytes):
            try:
                raw_string = raw_string.decode()
            except UnicodeDecodeError:
                return [(STRING, tokval)]
        encoded = ""
        for c in raw_string:
            ucode = f"\\u{hex(ord(c))[2:]:0>4}" if not c.isdigit() else c  # noqa: FURB116
            encoded += ucode
        return [(STRING, f"'{encoded}'")]

    @staticmethod
    def _additions(tokval: str):
        # "Hello, world!" --> "Hello, "+"world!"
        if len(tokval) < 6:  # noqa: PLR2004
            return [(STRING, tokval)]

        raw_string = False
        if tokval.startswith("r"):
            tokval = tokval[1:]
            raw_string = True

        symbols = tokval[-1]
        first_symbol = symbols
        if raw_string:
            first_symbol = "r" + first_symbol
        last_symbol = symbols
        s = random.randint(2, len(tokval) - 4)
        string_1 = first_symbol + tokval[1:s] + last_symbol
        string_2 = first_symbol + tokval[s:-1] + last_symbol
        return [
            (STRING, string_1),
            (OP, "+"),
            (STRING, string_2),
        ]

    @staticmethod
    def _only_additions(tokval: str):
        # "Hello, world!" --> "Hello, "+"world!"
        if len(tokval) <= 2:  # noqa: PLR2004
            return [(STRING, tokval)]

        raw_string = False
        if tokval.startswith("r"):
            tokval = tokval[1:]
            raw_string = True

        symbols = tokval[-1]
        first_symbol = symbols
        if raw_string:
            first_symbol = "r" + first_symbol
        last_symbol = symbols
        t = []
        add_slash = False
        for char in tokval[1:-1]:
            if char != "\\" and not add_slash:
                t.extend(
                    [
                        (STRING, first_symbol + char + last_symbol),
                        (OP, "+"),
                    ],
                )
            elif add_slash:
                t.extend(
                    [
                        (STRING, first_symbol + "\\" + char + last_symbol),
                        (OP, "+"),
                    ],
                )
                add_slash = False
            else:
                add_slash = True
        if t:
            t.pop()  # remove last +
        else:
            return [(STRING, tokval)]
        return t

    @staticmethod
    def _string_replace(tokval: str):
        raw_string = eval(tokval)  # noqa: S307

        if not raw_string or isinstance(raw_string, (str, bytes)):
            return [(STRING, tokval)]

        i = random.randint(0, len(raw_string) - 1)
        j = random.randint(i + 1, len(raw_string))
        original = raw_string[i:j]

        # TODO (deoktr): add option to change the generator
        generator = AdvancedGenerator.realistic_generator()
        new = next(generator)
        retries = 0
        max_retries = 5
        while new in raw_string:
            if retries >= max_retries:
                msg = "unable to generate a string that wasn't present in the original"
                raise PofError(msg)
            new = next(generator)
            retries += 1

        new_string = raw_string.replace(original, new)

        return [
            (STRING, repr(new_string)),
            (OP, "."),
            (NAME, "replace"),
            (OP, "("),
            (STRING, repr(new)),
            (OP, ","),
            (STRING, repr(original)),
            (OP, ")"),
        ]

    @staticmethod
    def _string_reverse(tokval: str):
        raw_string = eval(tokval)  # noqa: S307
        reversed_string = raw_string[::-1]
        return [
            (STRING, repr(reversed_string)),
            (OP, "["),
            (OP, ":"),
            (OP, ":"),
            (NUMBER, "-1"),
            (OP, "]"),
        ]

    @staticmethod
    def _string_one_on_n(tokval: str):
        """One on N.

        "".join([l if x%2 ==0 else "" for x, l in
            enumerate("Heeeleleoe,e eweoerelede!e")])
        """
        raw_string = eval(tokval)  # noqa: S307
        if not raw_string or isinstance(raw_string, bytes):
            return [(STRING, tokval)]

        # steps between each actual characters
        steps = random.randint(1, 7)

        obf_string = ""
        for char in raw_string:
            t = "".join(
                random.choices(
                    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890",
                    k=(steps - 1),
                ),
            )
            obf_string += char + t

        var_x = random.choice("abcdefghijklmnopqrstuvwxyz")
        var_l = random.choice("abcdefghijklmnopqrstuvwxyz")

        return [
            (STRING, '""'),
            (OP, "."),
            (NAME, "join"),
            (LPAR, "("),
            (OP, "["),
            (NAME, var_l),
            (NAME, "if"),
            (NAME, var_x),
            (OP, "%"),
            (NUMBER, str(steps)),
            (OP, "=="),
            (NUMBER, "0"),
            (NAME, "else"),
            (STRING, '""'),
            (NAME, "for"),
            (NAME, var_x),
            (OP, ","),
            (NAME, var_l),
            (NAME, "in"),
            (NAME, "enumerate"),
            (LPAR, "("),
            (STRING, repr(obf_string)),
            (RPAR, ")"),
            (OP, "]"),
            (OP, ")"),
        ]

    def _obfuscate_string(self, tokval: str, next_tokval: str):  # noqa: C901, PLR0912
        # TODO (deoktr): consider f"" u"" ur"" b"" r"" strings
        # consider empty strings
        # consider calling function on whole string "".format()
        is_bytes = self._is_bytes_literal(tokval)

        strategies = list(self.ALL)

        if is_bytes:
            # SHIFT and REPLACE are text-only; exclude for byte literals
            for s in (self.Strats.SHIFT, self.Strats.REPLACE):
                if s in strategies:
                    strategies.remove(s)

        if next_tokval != ".":
            strategies.append(self.Strats.HEX)
            if not is_bytes:
                # UNICODE uses \u escapes which are invalid in byte literals
                strategies.append(self.Strats.UNICODE)
                strategies.append(self.Strats.SHIFT)

        strategy = random.choice(strategies)

        if strategy == self.Strats.BASE64:
            tokens = self._obf_base64(tokval)
        elif strategy == self.Strats.ADDITION:
            tokens = self._additions(tokval)
        elif strategy == self.Strats.ONLY_ADDITION:
            tokens = self._only_additions(tokval)
        elif strategy == self.Strats.BASE85:
            tokens = self._obf_base85(tokval)
        elif strategy == self.Strats.HEX:
            tokens = self._hex(tokval)
        elif strategy == self.Strats.UNICODE:
            tokens = self._unicode(tokval)
        elif strategy == self.Strats.SHIFT:
            tokens = self._obf_shift(tokval)
        elif strategy == self.Strats.REPLACE:
            tokens = self._string_replace(tokval)
        elif strategy == self.Strats.REVERSE:
            tokens = self._string_reverse(tokval)
        elif strategy == self.Strats.ONE_ON_N:
            tokens = self._string_one_on_n(tokval)
        else:
            logger.error("unsupported strategy %s, not obfuscating", strategy)
            return [(STRING, tokval)]

        return tokens

    def obfuscate_tokens(self, tokens):
        tokens = merge_implicit_strings(tokens)
        result = []  # obfuscated tokens

        if self.import_b64decode:
            if self.b64decode_name != "b64decode":
                result.extend(
                    [
                        (NAME, "from"),
                        (NAME, "base64"),
                        (NAME, "import"),
                        (NAME, "b64decode"),
                        (NAME, "as"),
                        (NAME, self.b64decode_name),
                        (NEWLINE, "\n"),
                    ],
                )
            else:
                result.extend(
                    [
                        (NAME, "from"),
                        (NAME, "base64"),
                        (NAME, "import"),
                        (NAME, "b64decode"),
                        (NEWLINE, "\n"),
                    ],
                )

        if self.import_b85decode:
            if self.b85decode_name != "b85decode":
                result.extend(
                    [
                        (NAME, "from"),
                        (NAME, "base64"),
                        (NAME, "import"),
                        (NAME, "b85decode"),
                        (NAME, "as"),
                        (NAME, self.b85decode_name),
                        (NEWLINE, "\n"),
                    ],
                )
            else:
                result.extend(
                    [
                        (NAME, "from"),
                        (NAME, "base64"),
                        (NAME, "import"),
                        (NAME, "b85decode"),
                        (NEWLINE, "\n"),
                    ],
                )

        prev_toknum = None
        for index, (toknum, tokval, *_) in enumerate(tokens):
            new_tokens = [(toknum, tokval)]
            next_tokval = None
            if len(tokens) > index + 1:
                _, next_tokval, *__ = tokens[index + 1]

            # don't obfuscate docstrings
            if toknum == STRING and prev_toknum not in [
                NEWLINE,
                DEDENT,
                INDENT,
                ENCODING,
            ]:
                try:
                    new_tokens = self._obfuscate_string(tokval, next_tokval)
                except Exception:  # noqa: BLE001
                    logger.warning("failed to obfuscate string token: %s", tokval[:50])

            if new_tokens:
                result.extend(new_tokens)
            prev_toknum = toknum
        return result
