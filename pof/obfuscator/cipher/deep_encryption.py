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

from base64 import b64encode
from tokenize import (
    DEDENT,
    INDENT,
    LPAR,
    NAME,
    NEWLINE,
    NL,
    OP,
    RPAR,
    STRING,
    untokenize,
)

from pof.logger import logger


class DeepEncryptionObfuscator:
    def __init__(self, encryption_depth=0) -> None:
        self.encryption_depth = encryption_depth

    @staticmethod
    def _nested_depth_at(tokens):
        nested = 0
        awaiting = False
        for i, (toknum, tokval) in enumerate(tokens):
            if toknum == NAME and tokval in ("def", "class") and nested == 0:
                awaiting = True
            if awaiting and toknum == INDENT:
                awaiting = False
                nested += 1
            elif nested > 0 and toknum == INDENT:
                nested += 1
            elif nested > 0 and toknum == DEDENT:
                nested -= 1
            yield i, nested

    @staticmethod
    def _is_empty_return(tokens, pos):
        """Check if the return at pos has no value (bare return)."""
        for j in range(pos + 1, len(tokens)):
            nt = tokens[j][0]
            if nt in (NEWLINE, NL):
                return True
            if nt != DEDENT:
                return False
        return True

    @classmethod
    def _replace_returns(cls, tokens):
        """Replace return with r= at the function body level.

        Returns inside nested def/class are left intact.
        """
        depths = dict(cls._nested_depth_at(tokens))
        result = []
        for i, (toknum, tokval) in enumerate(tokens):
            if toknum == NAME and tokval == "return" and depths.get(i, 0) == 0:
                result.extend([(NAME, "r"), (OP, "=")])
                if cls._is_empty_return(tokens, i):
                    result.append((NAME, "None"))
            else:
                result.append((toknum, tokval))
        return result

    def obfuscate_tokens(self, tokens):  # noqa: C901 PLR0912
        """Encrypt every function's source code.

        Encrypt every function's source code and decrypt only when needed
        (just-in-time) via exec(). This prevents the entire source code being
        accessible at once in memory.

        Convert functions into the following:

        ```
        def function():
            r_dict=globals().copy()
            r_dict.update(locals())
            exec(b64decode(b'base64functioncode...'), r_dict)
            if'r'not in r_dict:
                return None
            r_val=r_dict['r']
            del r_dict
            return r_val
        ```
        """
        result = []  # obfuscated tokens
        result.extend(
            [
                (NAME, "from"),
                (NAME, "base64"),
                (NAME, "import"),
                (NAME, "b64decode"),
                (NEWLINE, "\n"),
            ],
        )
        depth = 0  # indent depth
        function_tokens = []
        function_def = False
        inside_function = False
        for index, (toknum, tokval, *_) in enumerate(tokens):
            new_tokens = [(toknum, tokval)]
            next_tokval = None
            if len(tokens) > index + 1:
                _next_toknum, next_tokval, *__ = tokens[index + 1]

            if toknum == INDENT:
                depth += 1
            elif toknum == DEDENT:
                depth -= 1

            if inside_function:
                function_tokens.append((toknum, tokval))
                new_tokens = []

            if tokval == "def" and toknum == NAME and depth == self.encryption_depth:
                logger.debug("function definition: %s", next_tokval)
                function_def = True
            elif function_def and toknum == OP and tokval == ":":
                function_def = False
                inside_function = True
            elif (
                inside_function and depth <= self.encryption_depth and toknum == DEDENT
            ):
                inside_function = False

                fixed_function_tokens = []
                fixed_depth = -1
                for ftnum, ftval in function_tokens:
                    ftval_d = ftval
                    if ftnum == INDENT:
                        fixed_depth += 1
                        ftval_d = fixed_depth * "    "
                    elif ftnum == DEDENT:
                        fixed_depth -= 1
                    fixed_function_tokens.append((ftnum, ftval_d))

                # [2:-1] removes the outer indent/dedent wrapper
                source = untokenize(fixed_function_tokens[2:-1])

                if not any(i in source for i in ["yield", "super"]):
                    body_tokens = fixed_function_tokens[2:-1]
                    replaced_tokens = self._replace_returns(body_tokens)
                    source = untokenize(replaced_tokens)

                    encoded = b64encode(source.encode())
                    globals_dict_name = "r_dict"
                    new_tokens = [
                        (NEWLINE, "\n"),
                        (INDENT, "    " * (self.encryption_depth + 1)),
                        # r_dict = globals().copy()
                        (NAME, globals_dict_name),
                        (OP, "="),
                        (NAME, "globals"),
                        (LPAR, "("),
                        (RPAR, ")"),
                        (OP, "."),
                        (NAME, "copy"),
                        (LPAR, "("),
                        (RPAR, ")"),
                        (NEWLINE, "\n"),
                        # r_dict.update(locals())
                        (NAME, globals_dict_name),
                        (OP, "."),
                        (NAME, "update"),
                        (LPAR, "("),
                        (NAME, "locals"),
                        (LPAR, "("),
                        (RPAR, ")"),
                        (RPAR, ")"),
                        (NEWLINE, "\n"),
                        # exec(b64decode(b'...'), r_dict)
                        (NAME, "exec"),
                        (LPAR, "("),
                        (NAME, "b64decode"),
                        (LPAR, "("),
                        (STRING, repr(encoded)),
                        (RPAR, ")"),
                        (OP, ","),
                        (NAME, globals_dict_name),
                        (RPAR, ")"),
                        (NEWLINE, "\n"),
                        # if 'r' not in r_dict:
                        (NAME, "if"),
                        (STRING, "'r'"),
                        (NAME, "not"),
                        (NAME, "in"),
                        (NAME, globals_dict_name),
                        (OP, ":"),
                        (NEWLINE, "\n"),
                        # return None
                        (INDENT, "    " * (self.encryption_depth + 2)),
                        (NAME, "return"),
                        (NAME, "None"),
                        (DEDENT, ""),
                        (NEWLINE, "\n"),
                        # r_val = r_dict['r']
                        (NAME, "r_val"),
                        (OP, "="),
                        (NAME, globals_dict_name),
                        (OP, "["),
                        (STRING, "'r'"),
                        (OP, "]"),
                        (NEWLINE, "\n"),
                        # del r_dict
                        (NAME, "del"),
                        (NAME, globals_dict_name),
                        (NEWLINE, "\n"),
                        # return r_val
                        (NAME, "return"),
                        (NAME, "r_val"),
                        (NEWLINE, "\n"),
                        (DEDENT, ""),
                    ]
                else:
                    new_tokens = function_tokens.copy()

                function_tokens = []

            if new_tokens:
                result.extend(new_tokens)

        return result
