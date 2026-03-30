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

from __future__ import annotations

import ast
import io
from tokenize import (
    COMMENT,
    DEDENT,
    ENDMARKER,
    INDENT,
    NAME,
    NEWLINE,
    NL,
    OP,
    generate_tokens,
)

from pof.utils.tokens import untokenize


class _Removal:
    """Describes a region of tokens to remove."""

    __slots__ = ("col", "kind", "line")

    def __init__(self, kind: str, line: int, col: int) -> None:
        self.kind = kind
        self.line = line
        self.col = col


class TypeHintsObfuscator:
    """Remove all type annotations from the code."""

    SKIP_TOKS = (NL, NEWLINE, INDENT, DEDENT, COMMENT)

    @staticmethod
    def _fill_empty_blocks(tokens: list) -> list:
        """Insert ``pass`` into block bodies left empty after removal."""
        filled: list = []
        for i, (toknum, tokval, *rest) in enumerate(tokens):
            filled.append((toknum, tokval, *rest))
            if toknum == INDENT:
                j = i + 1
                while j < len(tokens) and tokens[j][0] in (NEWLINE, NL, COMMENT):
                    j += 1
                if j < len(tokens) and tokens[j][0] == DEDENT:
                    filled.append((NAME, "pass"))
                    filled.append((NEWLINE, "\n"))
        return filled

    @classmethod
    def obfuscate_tokens(cls, tokens: list) -> list:
        source = untokenize(tokens)
        if isinstance(source, bytes):
            source = source.decode("utf-8")

        try:
            tree = ast.parse(source)
        except SyntaxError:
            return tokens

        removals = cls._collect_removals(tree)
        fresh = list(generate_tokens(io.StringIO(source).readline))
        result = cls._apply_removals(fresh, removals)
        return cls._fill_empty_blocks(result)

    @classmethod
    def _collect_removals(cls, tree: ast.AST) -> list[_Removal]:
        """Walk the AST and collect annotation sites to remove."""
        removals: list[_Removal] = []

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if node.returns is not None:
                    removals.append(
                        _Removal(
                            "return_ann",
                            node.returns.lineno,
                            node.returns.col_offset,
                        ),
                    )
                all_args = node.args.args + node.args.posonlyargs + node.args.kwonlyargs
                removals.extend(
                    _Removal(
                        "param_ann",
                        arg.lineno,
                        arg.col_offset + len(arg.arg),
                    )
                    for arg in all_args
                    if arg.annotation is not None
                )
                removals.extend(
                    _Removal(
                        "param_ann",
                        sp.lineno,
                        sp.col_offset + len(sp.arg),
                    )
                    for sp in (node.args.vararg, node.args.kwarg)
                    if sp and sp.annotation is not None
                )

            elif isinstance(node, ast.AnnAssign):
                if node.value is not None:
                    removals.append(
                        _Removal(
                            "var_ann",
                            node.lineno,
                            node.col_offset,
                        ),
                    )
                else:
                    removals.append(
                        _Removal(
                            "bare_ann",
                            node.lineno,
                            node.col_offset,
                        ),
                    )

        return removals

    @classmethod
    def _skip_type_expr(cls, tokens: list, i: int, n: int, stops: set[str]) -> int:
        """Advance past a type expression, respecting bracket nesting.

        Returns the index of the first stop-token at depth 0.
        """
        depth = 0
        while i < n:
            tn, tv = tokens[i][0], tokens[i][1]
            if tn == OP and tv in ("[", "("):
                depth += 1
            elif tn == OP and tv in ("]", ")"):
                if depth > 0:
                    depth -= 1
                else:
                    break
            elif depth == 0 and tn == OP and tv in stops:
                break
            i += 1
        return i

    @classmethod
    def _apply_removals(  # noqa: C901
        cls,
        tokens: list,
        removals: list[_Removal],
    ) -> list:
        """Filter the token stream based on collected removal info."""
        return_pos: set[tuple[int, int]] = set()
        param_pos: set[tuple[int, int]] = set()
        var_pos: set[tuple[int, int]] = set()
        bare_lines: set[int] = set()

        for r in removals:
            if r.kind == "return_ann":
                return_pos.add((r.line, r.col))
            elif r.kind == "param_ann":
                param_pos.add((r.line, r.col))
            elif r.kind == "var_ann":
                var_pos.add((r.line, r.col))
            elif r.kind == "bare_ann":
                bare_lines.add(r.line)

        result: list = []
        i = 0
        n = len(tokens)

        while i < n:
            toknum, tokval, start, _end, _line = tokens[i]
            srow = start[0]

            # bare annotation: remove entire logical line
            if srow in bare_lines and toknum not in (
                NEWLINE,
                NL,
                INDENT,
                DEDENT,
                ENDMARKER,
                COMMENT,
            ):
                while i < n and tokens[i][0] not in (NEWLINE, NL, ENDMARKER):
                    i += 1
                continue

            # return annotation: `-> type :`
            if (
                toknum == OP
                and tokval == "->"
                and cls._is_return_arrow(tokens, i, return_pos)
            ):
                i = cls._skip_type_expr(tokens, i + 1, n, {":"})
                continue

            # parameter annotation: `: type [, ) =]`
            if (
                toknum == OP
                and tokval == ":"
                and cls._is_param_colon(tokens, i, param_pos)
            ):
                i = cls._skip_type_expr(tokens, i + 1, n, {",", "=", ")"})
                continue

            # variable annotation with assignment `: type =`
            if (
                toknum == OP
                and tokval == ":"
                and cls._is_var_ann_colon(tokens, i, var_pos)
            ):
                i = cls._skip_type_expr(tokens, i + 1, n, {"="})
                if result and result[-1][0] == NAME and i < n:
                    result.append((NAME, ""))
                continue

            result.append((toknum, tokval))
            i += 1

        return result

    @classmethod
    def _is_return_arrow(
        cls,
        tokens: list,
        idx: int,
        positions: set[tuple[int, int]],
    ) -> bool:
        """Check if `->` at idx is a return type annotation arrow."""
        j = idx + 1
        while j < len(tokens) and tokens[j][0] in cls.SKIP_TOKS:
            j += 1
        if j < len(tokens):
            s = tokens[j][2]
            if (s[0], s[1]) in positions:
                return True
        return False

    @classmethod
    def _is_param_colon(
        cls,
        tokens: list,
        idx: int,
        positions: set[tuple[int, int]],
    ) -> bool:
        """Check if `:` at idx is a parameter type annotation colon."""
        prev = idx - 1
        while prev >= 0 and tokens[prev][0] in cls.SKIP_TOKS:
            prev -= 1
        if prev >= 0 and tokens[prev][0] == NAME:
            e = tokens[prev][3]
            if (e[0], e[1]) in positions:
                return True
        return False

    @classmethod
    def _is_var_ann_colon(
        cls,
        tokens: list,
        idx: int,
        positions: set[tuple[int, int]],
    ) -> bool:
        """Check if `:` at idx is a variable annotation colon."""
        prev = idx - 1
        while prev >= 0 and tokens[prev][0] in cls.SKIP_TOKS:
            prev -= 1
        if prev >= 0 and tokens[prev][0] == NAME:
            s = tokens[prev][2]
            if (s[0], s[1]) in positions:
                return True
        return False
