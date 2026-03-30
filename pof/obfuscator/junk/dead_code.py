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
from collections.abc import Generator
from tokenize import (
    COMMENT,
    DEDENT,
    INDENT,
    NAME,
    NEWLINE,
    NL,
    NUMBER,
    OP,
    STRING,
)

from pof.utils.generator import BasicGenerator


class DeadCodeObfuscator:
    """Insert dead (unreachable/unused) code blocks into the source."""

    VALID_STATEMENT_TYPES = (
        "function",
        "if",
        "for",
        "while",
        "assignment",
    )

    def __init__(  # noqa: PLR0913
        self,
        frequency: float = 0.3,
        max_function_depth: int = 2,
        max_branches: int = 3,
        statement_types: list[str] | None = None,
        generate_classes: bool = False,  # noqa: FBT001, FBT002
        generator: Generator[str] | None = None,
    ) -> None:
        self.frequency: float = frequency
        self.max_function_depth: int = max_function_depth
        self.max_branches: int = max_branches
        self.generate_classes: bool = generate_classes

        if statement_types is not None:
            self.statement_types: list[str] = [
                s for s in statement_types if s in self.VALID_STATEMENT_TYPES
            ]
        else:
            self.statement_types = list(self.VALID_STATEMENT_TYPES)

        if generator is None:
            generator = BasicGenerator.function_generator()
        self.generator: Generator[str] = generator
        self._var_generator: Generator[str] = BasicGenerator.alphabet_generator()

    def _next_name(self) -> str:
        return next(self.generator)

    def _next_var(self) -> str:
        return next(self._var_generator)

    @staticmethod
    def _collect_existing_names(tokens) -> set[str]:
        names: set[str] = set()
        for toknum, tokval, *_ in tokens:
            if toknum == NAME:
                names.add(tokval)
        return names

    def _random_expr_tokens(self):
        choice = random.randint(0, 3)
        if choice == 0:
            a, b = random.randint(1, 999), random.randint(1, 999)
            op = random.choice(["+", "-", "*", "%"])
            return [(NUMBER, str(a)), (OP, op), (NUMBER, str(b))]
        if choice == 1:
            words = ["data", "info", "temp", "cache", "buf", "msg", "tag"]
            return [(STRING, repr(random.choice(words)))]
        if choice == 2:  # noqa: PLR2004
            items = [random.randint(0, 100) for _ in range(random.randint(1, 4))]
            tokens = [(OP, "[")]
            for i, item in enumerate(items):
                if i > 0:
                    tokens.append((OP, ","))
                tokens.append((NUMBER, str(item)))
            tokens.append((OP, "]"))
            return tokens
        return [(NUMBER, str(random.randint(0, 9999)))]

    def _body_tokens(self, count: int = 0):
        """Generate body tokens for a block (assignments)."""
        if count == 0:
            count = random.randint(1, 3)
        tokens = []
        for _ in range(count):
            var = self._next_var()
            tokens.append((NAME, var))
            tokens.append((OP, "="))
            tokens.extend(self._random_expr_tokens())
            tokens.append((NEWLINE, "\n"))
        return tokens

    def _generate_dead_function_tokens(self, indent_level: int, depth: int):
        fname = self._next_name()
        params = [self._next_var() for _ in range(random.randint(0, 3))]
        inner_indent = "    " * (indent_level + 1)

        tokens = [
            (NAME, "def"),
            (NAME, fname),
            (OP, "("),
        ]
        for i, p in enumerate(params):
            if i > 0:
                tokens.append((OP, ","))
            tokens.append((NAME, p))
        tokens.extend(
            [
                (OP, ")"),
                (OP, ":"),
                (NEWLINE, "\n"),
                (INDENT, inner_indent),
            ],
        )
        tokens.extend(self._body_tokens())

        if depth < self.max_function_depth and random.random() < 0.3:  # noqa: PLR2004
            tokens.extend(
                self._generate_dead_function_tokens(indent_level + 1, depth + 1),
            )

        tokens.append((DEDENT, ""))
        return tokens

    @staticmethod
    def _get_false_cond():
        false_conds = [
            [(NAME, "False")],
            [(NUMBER, "0")],
            [(STRING, '""')],
            [(NAME, "None")],
            [
                (NUMBER, str(random.randint(1, 50))),
                (OP, ">"),
                (NUMBER, str(random.randint(51, 100))),
            ],
            [
                (NUMBER, str(random.randint(1, 50))),
                (OP, "=="),
                (NUMBER, str(random.randint(51, 100))),
            ],
            [(NAME, "not"), (NAME, "True")],
            [(NAME, "True"), (NAME, "and"), (NAME, "False")],
            [(NUMBER, "0"), (OP, "*"), (NUMBER, str(random.randint(1, 999)))],
            [(NAME, "len"), (OP, "("), (STRING, '""'), (OP, ")")],
            [(NAME, "bool"), (OP, "("), (NUMBER, "0"), (OP, ")")],
            [(OP, "("), (OP, ")"), (NAME, "and"), (NAME, "True")],
        ]
        return random.choice(false_conds)

    def _generate_dead_if_tokens(self, indent_level: int):
        inner_indent = "    " * (indent_level + 1)

        tokens = [(NAME, "if")]
        tokens.extend(self._get_false_cond())
        tokens.extend(
            [
                (OP, ":"),
                (NEWLINE, "\n"),
                (INDENT, inner_indent),
            ],
        )
        tokens.extend(self._body_tokens())
        tokens.append((DEDENT, ""))

        num_elif = random.randint(0, max(0, self.max_branches - 1))
        for _ in range(num_elif):
            tokens.append((NAME, "elif"))
            tokens.extend(self._get_false_cond())
            tokens.extend(
                [
                    (OP, ":"),
                    (NEWLINE, "\n"),
                    (INDENT, inner_indent),
                ],
            )
            tokens.extend(self._body_tokens())
            tokens.append((DEDENT, ""))

        return tokens

    def _generate_dead_for_tokens(self, indent_level: int):
        var = self._next_var()
        inner_indent = "    " * (indent_level + 1)

        empty_choices = [
            [(OP, "["), (OP, "]")],
            [(NAME, "range"), (OP, "("), (NUMBER, "0"), (OP, ")")],
            [(OP, "("), (OP, ")")],
            [(OP, "{"), (OP, "}")],
            [(STRING, '""')],
            [(NAME, "set"), (OP, "("), (OP, ")")],
        ]

        tokens = [
            (NAME, "for"),
            (NAME, var),
            (NAME, "in"),
        ]
        tokens.extend(random.choice(empty_choices))
        tokens.extend(
            [
                (OP, ":"),
                (NEWLINE, "\n"),
                (INDENT, inner_indent),
            ],
        )
        tokens.extend(self._body_tokens())
        tokens.append((DEDENT, ""))
        return tokens

    def _generate_dead_while_tokens(self, indent_level: int):
        inner_indent = "    " * (indent_level + 1)
        tokens = [(NAME, "while")]
        tokens.extend(self._get_false_cond())
        tokens.extend(
            [
                (OP, ":"),
                (NEWLINE, "\n"),
                (INDENT, inner_indent),
            ],
        )
        tokens.extend(self._body_tokens())
        tokens.append((DEDENT, ""))
        return tokens

    def _generate_dead_class_tokens(self, indent_level: int):
        cname = self._next_name().capitalize()
        inner_indent = "    " * (indent_level + 1)
        tokens = [
            (NAME, "class"),
            (NAME, cname),
            (OP, ":"),
            (NEWLINE, "\n"),
            (INDENT, inner_indent),
        ]
        tokens.extend(self._generate_dead_function_tokens(indent_level + 1, 0))
        tokens.append((DEDENT, ""))
        return tokens

    def _generate_dead_assignment_tokens(self):
        var = self._next_var()
        tokens = [
            (NAME, var),
            (OP, "="),
        ]
        tokens.extend(self._random_expr_tokens())
        tokens.append((NEWLINE, "\n"))
        return tokens

    def _generate_dead_code(self, indent_level: int):
        """Generate a dead code block and return its tokens."""
        available = list(self.statement_types)
        if self.generate_classes:
            available.append("class")

        if indent_level > 0:
            weights = []
            for t in available:
                if t in ("function", "class"):
                    weights.append(1)
                else:
                    weights.append(3)
        else:
            weights = [1] * len(available)

        choice = random.choices(available, weights=weights, k=1)[0]
        match choice:
            case "function":
                return self._generate_dead_function_tokens(indent_level, 0)
            case "if":
                return self._generate_dead_if_tokens(indent_level)
            case "for":
                return self._generate_dead_for_tokens(indent_level)
            case "while":
                return self._generate_dead_while_tokens(indent_level)
            case "class":
                return self._generate_dead_class_tokens(indent_level)
            case _:
                return self._generate_dead_assignment_tokens()

    def obfuscate_tokens(self, tokens):  # noqa: C901
        existing: set[str] = self._collect_existing_names(tokens)
        BasicGenerator.extend_reserved(list(existing))

        result = []
        indent_level: int = 0
        paren_depth: int = 0
        in_decorator: bool = False

        for idx, (toknum, tokval, *_) in enumerate(tokens):
            if toknum == INDENT:
                indent_level += 1
            elif toknum == DEDENT:
                indent_level = max(0, indent_level - 1)

            if toknum == OP and tokval in ("(", "[", "{"):
                paren_depth += 1
            elif toknum == OP and tokval in (")", "]", "}"):
                paren_depth = max(0, paren_depth - 1)

            if toknum == OP and tokval == "@":
                in_decorator = True
            if in_decorator and toknum == NAME and tokval in ("def", "class"):
                in_decorator = False

            result.append((toknum, tokval))

            # do NOT insert if an INDENT is upcoming (possibly after NL/COMMENT
            # tokens), that would break the block header (def/if/for/while/
            # class/try) by placing code between the header's NEWLINE and the
            # body's INDENT
            if (
                toknum == NEWLINE
                and paren_depth == 0
                and not in_decorator
                and random.random() < self.frequency
            ):
                has_upcoming_indent = False
                for j in range(idx + 1, len(tokens)):
                    upcoming = tokens[j][0]
                    if upcoming in (NL, COMMENT):
                        continue
                    if upcoming == INDENT:
                        has_upcoming_indent = True
                    break
                if not has_upcoming_indent:
                    dead_tokens = self._generate_dead_code(indent_level)
                    result.extend(dead_tokens)

        return result
