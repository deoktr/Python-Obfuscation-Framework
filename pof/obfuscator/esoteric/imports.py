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

from tokenize import ENDMARKER, NAME, NEWLINE, NL, OP, STRING


class ImportsObfuscator:
    """Obfuscate import statements using __import__().

    Supported forms:

    ```
    # import X
    X = __import__("X")

    # import X as Y
    Y = __import__("X")

    # import X, Y
    X = __import__("X")
    Y = __import__("Y")

    # import X.Y
    X = __import__("X.Y")

    # from X import Y
    Y = __import__("X", fromlist=["Y"]).Y

    # from X import Y as Z
    Z = __import__("X", fromlist=["Y"]).Y

    # from X import Y, Z
    Y = __import__("X", fromlist=["Y"]).Y
    Z = __import__("X", fromlist=["Z"]).Z
    ```

    Left unchanged:

    ```
    from X import *
    from . import X
    ```
    """

    @staticmethod
    def _is_statement_start(preceding_tokens: list) -> bool:
        """Check if the current position is a valid statement start."""
        if not preceding_tokens:
            return True
        for toknum, _ in reversed(preceding_tokens):
            if toknum in (NEWLINE, NL, ENDMARKER):
                return True
            if toknum in (NAME, OP, STRING):
                return False
        return True

    @classmethod
    def _transform_import(cls, stmt_tokens: list) -> list | None:
        """Transform collected import statement tokens into __import__() calls.

        Returns None if the import should be left unchanged.
        """
        body = [
            (t, v)
            for t, v in stmt_tokens
            if t not in (NEWLINE, NL, ENDMARKER) and v not in ("(", ")")
        ]
        trailing = [(t, v) for t, v in stmt_tokens if t in (NEWLINE, NL, ENDMARKER)]

        if not body:
            return None

        first_val = body[0][1]

        if first_val == "import":
            return cls._transform_simple_import(body[1:]) + trailing
        if first_val == "from":
            t = cls._transform_from_import(body[1:])
            if t is None:
                return None
            return t + trailing
        return None

    @classmethod
    def _transform_simple_import(cls, tokens: list) -> list:
        """Transform: import X / import X as Y / import X, Y / import X.Y."""
        groups = cls._split_by_comma(tokens)
        result: list = []

        for group in groups:
            if not group:
                continue
            if result:
                result.append((NEWLINE, "\n"))

            names, alias = cls._extract_alias(group)
            module_name = cls._join_dotted_name(names)
            bind_name = alias or names[0][1]

            result.extend(
                [
                    (NAME, bind_name),
                    (OP, "="),
                    (NAME, "__import__"),
                    (OP, "("),
                    (STRING, repr(module_name)),
                    (OP, ")"),
                ],
            )

        return result

    @classmethod
    def _transform_from_import(cls, tokens: list) -> list | None:
        """Transform: from X import Y / from X import Y as Z / from X import Y, Z.

        Returns None for relative imports or wildcard imports.
        """
        import_idx = None
        for idx, (_, v) in enumerate(tokens):
            if v == "import":
                import_idx = idx
                break

        if import_idx is None:
            return None

        module_tokens = tokens[:import_idx]
        name_tokens = tokens[import_idx + 1 :]

        if any(v == "." for _, v in module_tokens):
            return None

        if any(v == "*" for _, v in name_tokens):
            return None

        module_name = cls._join_dotted_name(module_tokens)

        groups = cls._split_by_comma(name_tokens)
        result: list = []

        for group in groups:
            if not group:
                continue
            if result:
                result.append((NEWLINE, "\n"))

            names, alias = cls._extract_alias(group)
            imported_name = names[0][1]
            bind_name = alias or imported_name

            result.extend(
                [
                    (NAME, bind_name),
                    (OP, "="),
                    (NAME, "__import__"),
                    (OP, "("),
                    (STRING, repr(module_name)),
                    (OP, ","),
                    (NAME, "fromlist"),
                    (OP, "="),
                    (OP, "["),
                    (STRING, repr(imported_name)),
                    (OP, "]"),
                    (OP, ")"),
                    (OP, "."),
                    (NAME, imported_name),
                ],
            )

        return result

    @staticmethod
    def _split_by_comma(tokens: list) -> list[list]:
        """Split a token list by comma operators."""
        groups: list[list] = [[]]
        for toknum, tokval in tokens:
            if toknum == OP and tokval == ",":
                groups.append([])
            else:
                groups[-1].append((toknum, tokval))
        return groups

    @staticmethod
    def _extract_alias(tokens: list) -> tuple[list, str | None]:
        """Extract name tokens and alias from a token group.

        Returns (name_tokens, alias_string_or_None).
        """
        alias = None
        name_tokens = []
        saw_as = False
        for toknum, tokval in tokens:
            if tokval == "as":
                saw_as = True
            elif saw_as:
                alias = tokval
                saw_as = False
            else:
                name_tokens.append((toknum, tokval))
        return name_tokens, alias

    @staticmethod
    def _join_dotted_name(tokens: list) -> str:
        """Join NAME and OP('.') tokens into a dotted module name string."""
        return "".join(v for _, v in tokens)

    @classmethod
    def obfuscate_tokens(cls, tokens: list) -> list:
        result: list = []
        i = 0
        while i < len(tokens):
            toknum, tokval, *_ = tokens[i]

            if (
                toknum == NAME
                and tokval in ("import", "from")
                and cls._is_statement_start(result)
            ):
                stmt_tokens = []
                j = i
                paren_depth = 0
                while j < len(tokens):
                    st, sv, *_ = tokens[j]
                    stmt_tokens.append((st, sv))
                    if sv == "(":
                        paren_depth += 1
                    elif sv == ")":
                        paren_depth -= 1
                    if st in (NEWLINE, NL, ENDMARKER) and paren_depth <= 0:
                        break
                    j += 1

                replacement = cls._transform_import(stmt_tokens)
                if replacement is not None:
                    result.extend(replacement)
                else:
                    result.extend(stmt_tokens)
                i = j + 1
                continue

            result.append((toknum, tokval))
            i += 1
        return result
