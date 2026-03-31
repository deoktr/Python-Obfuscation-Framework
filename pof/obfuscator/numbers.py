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

import random
from enum import Enum
from tokenize import (
    COMMA,
    FSTRING_END,
    FSTRING_START,
    LPAR,
    NAME,
    NUMBER,
    OP,
    PLUS,
    RPAR,
    STRING,
    untokenize,
)

from pof.errors import PofError
from pof.logger import logger


class NumberObfuscator:
    """Obfuscate numbers with multiple methods."""

    class NStrats(Enum):
        STRING = 1
        ADDITION = 2
        HEX = 3
        BOOLEAN = 4
        LEN = 5
        BITWISE = 6

    INT_STRATS = (  # positive int obfuscation strategies
        NStrats.STRING,
        NStrats.ADDITION,
        NStrats.HEX,
        NStrats.BITWISE,
    )
    NEG_INT_STRATS = (  # negative int obfuscation strategies
        NStrats.STRING,
        NStrats.ADDITION,
        NStrats.HEX,
        NStrats.BITWISE,
    )
    FLOAT_STRATS = (  # positive float obfuscation strategies
        NStrats.STRING,
        NStrats.ADDITION,
    )
    NEG_FLOAT_STRATS = (  # negative float obfuscation strategies
        NStrats.STRING,
        NStrats.ADDITION,  # FIXME (deoktr): may fail, for example: 3.3 != 1.1 + 2.2
    )

    # TODO (deoktr): add frequency for each techniques, this may be a bit more difficult
    # compare to other classes because in this case it depend on the format of
    # the number, so maybe have a "global_frequency" or something like that,
    # that would enable or disable the obfuscation for any given number, then
    # the choice of method is based on their individual frequencies
    def __init__(self) -> None:
        self.number_list = []

    @staticmethod
    def obf_addition(tokval, tok_actual_val, token_type):
        # can fail, for example with 0o755 (file perm)
        # obfuscate number with additions
        a = random.randint(0, max(token_type(tokval), random.randint(2, 8)))
        b = tok_actual_val - a
        token_a = [
            (NUMBER, str(a)),
        ]
        if a < 0:
            token_a = [
                (LPAR, "("),
                *token_a,
                (RPAR, ")"),
            ]
        token_b = [
            (NUMBER, str(b)),
        ]
        if b < 0:
            token_b = [
                (LPAR, "("),
                *token_b,
                (RPAR, ")"),
            ]
        # randomize order
        tokens = [
            *token_a,
            (PLUS, "+"),
            *token_b,
        ]
        if token_type is int:
            tokens = [
                (NAME, "int"),
                (LPAR, "("),
                *tokens,
                (RPAR, ")"),
            ]
        elif token_type is float:
            tokens = [
                (NAME, "round"),
                (LPAR, "("),
                *tokens,
                (COMMA, ","),
                (NUMBER, "12"),
                (RPAR, ")"),
            ]
        return [
            (LPAR, "("),
            *tokens,
            (RPAR, ")"),
        ]

    @staticmethod
    def obf_hex_conversion(tokval):
        # only works for int
        # int('0Xff', 0) = 255
        hex_val = hex(int(tokval))
        return [
            (NAME, "int"),
            (LPAR, "("),
            (STRING, f"'{hex_val!s}'"),
            (COMMA, ","),
            (NUMBER, "0"),
            (RPAR, ")"),
        ]

    @staticmethod
    def obf_string_conversion(tokval, token_type):
        # 2 --> int('2')
        # 4.2 --> float('4.2')
        # useful for further string obfuscation or even builtin obfuscation
        if token_type is int:
            t = "int"
        elif token_type is float:
            t = "float"
        else:
            msg = f"{token_type=} not supported"
            logger.error(msg)
        return [
            (NAME, t),
            (LPAR, "("),
            (STRING, f"'{tokval}'"),
            (RPAR, ")"),
        ]

    @staticmethod
    def obf_boolean_conversion(tokval):
        # 42 --> (True + True + True ...)
        # True = 1
        # this obfuscation is hardcode ! and combined with builtin obfuscation
        # afterward it can be pretty messy, and leave HUGE chunk dedicated to
        # generating a single number !
        t = [(LPAR, "(")]
        for _ in range(int(tokval)):
            t.extend(
                [
                    (NAME, "True"),
                    (OP, "+"),
                ],
            )
        t.pop()  # remove last +  yeah dirty... I know
        t.append((RPAR, ")"))
        return t

    @staticmethod
    def obf_len_random(tokval):
        # create random obfjects which len is equal to the tokval
        # will of course only work for integers
        # the drawback is that it doesn't scale very well AT ALL
        value = int(tokval)
        is_positiv = value >= 0

        # TODO (deoktr): make the obf_tokens fully random, could be list, dict
        letter = random.choice("abcdefghijklmnopqrstuvwxyz")
        string = letter * abs(value)
        obf_tokens = [(STRING, repr(string))]

        t = []
        if not is_positiv:
            t.append((OP, "-"))
        t.extend(
            [
                (NAME, "len"),
                (LPAR, "("),
                *obf_tokens,
                (RPAR, ")"),
            ],
        )
        return t

    @staticmethod
    def obf_bitwise(tokval):  # noqa: C901, PLR0912
        """Obfuscate integer using bitwise operations."""
        n = int(tokval)

        # choose a sub-strategy randomly
        strategies = ["xor", "shift", "not"]
        if n != 0:
            strategies.append("or_compose")
        strategy = random.choice(strategies)

        if strategy == "xor":
            # n = a ^ b where a is random, b = n ^ a
            mask = random.randint(1, max(abs(n) + 100, 255))
            other = n ^ mask
            tokens = [
                (NUMBER, str(mask)),
                (OP, "^"),
            ]
            if other < 0:
                tokens.extend(
                    [
                        (LPAR, "("),
                        (NUMBER, str(other)),
                        (RPAR, ")"),
                    ],
                )
            else:
                tokens.append((NUMBER, str(other)))

        elif strategy == "shift":
            if n == 0:
                # 1 >> 1 = 0
                tokens = [
                    (NUMBER, "1"),
                    (OP, ">>"),
                    (NUMBER, "1"),
                ]
            elif n > 0:
                # find a valid shift amount
                k = random.randint(1, 3)
                shifted = n >> k
                remainder = n - (shifted << k)
                if remainder == 0:
                    tokens = [
                        (NUMBER, str(shifted)),
                        (OP, "<<"),
                        (NUMBER, str(k)),
                    ]
                else:
                    tokens = [
                        (LPAR, "("),
                        (NUMBER, str(shifted)),
                        (OP, "<<"),
                        (NUMBER, str(k)),
                        (RPAR, ")"),
                        (OP, "|"),
                        (NUMBER, str(remainder)),
                    ]
            else:
                # for negatives, use ~(~n)
                complement = ~n
                tokens = [
                    (OP, "~"),
                    (NUMBER, str(complement)),
                ]

        elif strategy == "not":
            # ~(~n) = n, but render as ~m where m = ~n
            complement = ~n
            if complement >= 0:
                tokens = [
                    (OP, "~"),
                    (NUMBER, str(complement)),
                ]
            else:
                tokens = [
                    (OP, "~"),
                    (LPAR, "("),
                    (NUMBER, str(complement)),
                    (RPAR, ")"),
                ]

        else:
            # or_compose: split n into disjoint bit groups
            # a | b where a & b == 0 and a | b == n
            if n > 0:
                bit_len = n.bit_length()
                split = random.randint(1, max(bit_len - 1, 1))
                mask = (1 << split) - 1
                a = n & mask
                b = n & ~mask
            else:
                # for negatives, use XOR as fallback
                mask = random.randint(1, 255)
                other = n ^ mask
                tokens = [
                    (NUMBER, str(mask)),
                    (OP, "^"),
                ]
                if other < 0:
                    tokens.extend(
                        [
                            (LPAR, "("),
                            (NUMBER, str(other)),
                            (RPAR, ")"),
                        ],
                    )
                else:
                    tokens.append((NUMBER, str(other)))
                return [
                    (LPAR, "("),
                    *tokens,
                    (RPAR, ")"),
                ]
            tokens = [
                (NUMBER, str(a)),
                (OP, "|"),
                (NUMBER, str(b)),
            ]

        return [
            (LPAR, "("),
            *tokens,
            (RPAR, ")"),
        ]

    @staticmethod
    def verify_number_obfuscation(tokval, tokens):
        # if only one token then it's the same
        if len(tokens) < 1:
            return False
        code = untokenize(tokens)
        result = eval(code)  # noqa: S307
        # logger.debug("verifying that {}={}".format(tokval, result))
        if str(result) == tokval:
            return True
        msg = f"error verifying that {tokval}={result}"
        logger.error(msg)
        return False

    def obfuscate_number(self, toknum, tokval):  # noqa: C901, PLR0912, PLR0915
        unobfuscated = [(toknum, tokval)]

        # get token type
        token_type = None
        tok_actual_val = None
        clean_tokval = tokval
        if tokval.startswith("-"):
            clean_tokval = clean_tokval.strip("-")
        if clean_tokval.isdigit():
            token_type = int
            tok_actual_val = int(tokval)
        else:
            try:
                tok_actual_val = float(tokval)
                token_type = float
            except ValueError:
                pass
        if token_type is None:
            return unobfuscated

        # get list of strats
        tok_positiv = tok_actual_val >= 0
        if tok_positiv and token_type is int:
            strategies = self.INT_STRATS
            if 2 < tok_actual_val < 100:  # noqa: PLR2004
                strategies = list(strategies)
                strategies.append(self.NStrats.LEN)
        elif not tok_positiv and token_type is int:
            strategies = self.NEG_INT_STRATS
            if 2 < tok_actual_val < 100:  # noqa: PLR2004
                strategies = list(strategies)
                strategies.append(self.NStrats.LEN)
        elif tok_positiv and token_type is float:
            strategies = self.FLOAT_STRATS
        elif not tok_positiv and token_type is float:
            strategies = self.NEG_FLOAT_STRATS

        if (
            token_type is int and tok_positiv and 2 < tok_actual_val < 100  # noqa: PLR2004
        ):
            strategies = list(strategies)
            strategies.append(self.NStrats.BOOLEAN)

        try:
            strategy = random.choice(strategies)

            if strategy == self.NStrats.STRING:
                tokens = self.obf_string_conversion(tokval, token_type)
            elif strategy == self.NStrats.ADDITION:
                tokens = self.obf_addition(tokval, tok_actual_val, token_type)
            elif strategy == self.NStrats.HEX:
                tokens = self.obf_hex_conversion(tokval)
            elif strategy == self.NStrats.BOOLEAN:
                tokens = self.obf_boolean_conversion(tokval)
            elif strategy == self.NStrats.LEN:
                tokens = self.obf_len_random(tokval)
            elif strategy == self.NStrats.BITWISE:
                tokens = self.obf_bitwise(tokval)
            else:
                msg = f"Strategy {strategy} not found"
                raise PofError(msg)  # noqa: TRY301

            if self.verify_number_obfuscation(tokval, tokens):
                return tokens

            msg = f"unable to verify obfuscation with: {tokens}."
            raise PofError(msg)  # noqa: TRY301
        except Exception as e:  # noqa: BLE001
            msg = f"unable to obfuscate number {tokval} with {strategy}: {e!s}"
            logger.exception(msg)
            # just in case we can't obfuscate it, for example if we have tokval
            # 0o755 all obfuscation method will fail
            return unobfuscated

    def obfuscate_tokens(self, tokens):  # noqa: C901
        result = []
        fstring_depth = 0
        prev_tokval = None
        in_case_pattern = False
        case_depth = 0
        for toknum, tokval, *_ in tokens:
            new_tokens = [(toknum, tokval)]

            if toknum == FSTRING_START:
                fstring_depth += 1
            elif toknum == FSTRING_END:
                fstring_depth -= 1

            if prev_tokval == "case":
                in_case_pattern = True
                case_depth = 0
            if in_case_pattern:
                if tokval in ("(", "[", "{"):
                    case_depth += 1
                elif tokval in (")", "]", "}"):
                    case_depth -= 1
                elif tokval == ":" and case_depth == 0:
                    in_case_pattern = False

            # don't obfuscate case pattern literals
            if toknum == NUMBER and fstring_depth == 0 and not in_case_pattern:
                new_tokens = self.obfuscate_number(toknum, tokval)

            if new_tokens:
                result.extend(new_tokens)
            prev_tokval = tokval
        return result
