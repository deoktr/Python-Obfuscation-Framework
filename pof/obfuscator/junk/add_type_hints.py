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
import random
from tokenize import (
    COMMENT,
    DEDENT,
    INDENT,
    NAME,
    NEWLINE,
    NL,
    OP,
    generate_tokens,
)

from pof.utils.tokens import untokenize


class _Injection:
    """Describes where and what to inject."""

    __slots__ = ("col", "kind", "line")

    def __init__(self, kind: str, line: int, col: int) -> None:
        self.kind = kind
        self.line = line
        self.col = col


class AddTypeHintsObfuscator:
    """Add random type hints to functions and variables."""

    GENERIC_BASES_1 = ("list", "set", "frozenset")
    GENERIC_BASES_2 = ("dict",)
    SKIP_TOKS = (NL, NEWLINE, INDENT, DEDENT, COMMENT)
    SIMPLE_TYPES = (
        "int",
        "str",
        "bytes",
        "bool",
        "float",
        "complex",
        "None",
        "object",
        "type",
        "memoryview",
        "bytearray",
        "range",
    )
    NON_NONE_SIMPLE = tuple(t for t in SIMPLE_TYPES if t != "None")

    def __init__(
        self,
        max_depth: int = 2,
        simple_weight: float = 0.45,
        generic_type_weight: float = 0.75,
        generic_prob: float = 0.6,
        union_split: float = 0.5,
    ) -> None:
        self.max_depth = max_depth
        self.simple_weight = simple_weight
        self.generic_weight = generic_type_weight
        self.generic_prob = generic_prob
        self.union_split = union_split

    @classmethod
    def _random_simple(cls) -> str:
        return random.choice(cls.SIMPLE_TYPES)

    def _random_type(self, depth: int = 0, *, allow_union: bool = True) -> str:
        """Generate a random type expression string."""
        if depth >= self.max_depth:
            return self._random_simple()

        roll = random.random()
        if roll < self.simple_weight:
            return self._random_simple()
        if roll < self.generic_weight or not allow_union:
            return self._random_generic(depth)
        # union type, exclude None to avoid runtime TypeError
        a = self._random_non_none(depth + 1)
        b = self._random_non_none(depth + 1)
        while b == a:
            b = self._random_non_none(depth + 1)
        return f"{a} | {b}"

    def _random_generic(self, depth: int) -> str:
        """Generate a random generic type expression."""
        if random.random() < self.generic_prob:
            base = random.choice(self.GENERIC_BASES_1)
            inner = self._random_type(depth + 1, allow_union=False)
            return f"{base}[{inner}]"

        base = random.choice(self.GENERIC_BASES_2)
        k = self._random_type(depth + 1, allow_union=False)
        v = self._random_type(depth + 1, allow_union=False)
        return f"{base}[{k}, {v}]"

    def _random_non_none(self, depth: int = 0) -> str:
        """Generate a random type that is not None (safe for | unions)."""
        if depth >= self.max_depth:
            return random.choice(self.NON_NONE_SIMPLE)
        if random.random() < self.union_split:
            return random.choice(self.NON_NONE_SIMPLE)
        return self._random_generic(depth)

    def obfuscate_tokens(self, tokens: list) -> list:
        source = untokenize(tokens)
        if isinstance(source, bytes):
            source = source.decode("utf-8")

        try:
            tree = ast.parse(source)
        except SyntaxError:
            return tokens

        injections = self._collect_injections(tree)
        if not injections:
            return tokens

        fresh = list(generate_tokens(io.StringIO(source).readline))
        return self._apply_injections(fresh, injections)

    @classmethod
    def _collect_injections(  # noqa: C901, PLR0912
        cls,
        tree: ast.AST,
    ) -> list[_Injection]:
        """Walk AST to find all annotation injection sites."""
        injections: list[_Injection] = []

        for node in ast.walk(tree):
            if isinstance(
                node,
                (ast.FunctionDef, ast.AsyncFunctionDef),
            ):
                # return annotation
                if node.returns is None:
                    # inject `->` before the body colon
                    injections.append(
                        _Injection(
                            "add_return",
                            node.lineno,
                            node.col_offset,
                        ),
                    )
                else:
                    injections.append(
                        _Injection(
                            "replace_return",
                            node.returns.lineno,
                            node.returns.col_offset,
                        ),
                    )

                # parameter annotations
                all_args = node.args.args + node.args.posonlyargs + node.args.kwonlyargs
                for arg in all_args:
                    if arg.arg in ("self", "cls"):
                        continue
                    if arg.annotation is None:
                        injections.append(
                            _Injection(
                                "add_param",
                                arg.lineno,
                                arg.col_offset + len(arg.arg),
                            ),
                        )
                    else:
                        injections.append(
                            _Injection(
                                "replace_param",
                                arg.lineno,
                                arg.col_offset + len(arg.arg),
                            ),
                        )

                for sp in (node.args.vararg, node.args.kwarg):
                    if sp is None:
                        continue
                    if sp.annotation is None:
                        injections.append(
                            _Injection(
                                "add_param",
                                sp.lineno,
                                sp.col_offset + len(sp.arg),
                            ),
                        )
                    else:
                        injections.append(
                            _Injection(
                                "replace_param",
                                sp.lineno,
                                sp.col_offset + len(sp.arg),
                            ),
                        )

            elif isinstance(node, ast.Assign):
                # simple name `=` value assignments only
                if len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
                    target = node.targets[0]
                    injections.append(
                        _Injection(
                            "add_var",
                            target.lineno,
                            target.col_offset + len(target.id),
                        ),
                    )

            elif isinstance(node, ast.AnnAssign):
                if (
                    node.annotation is not None
                    and node.target is not None
                    and isinstance(node.target, ast.Name)
                ):
                    injections.append(
                        _Injection(
                            "replace_var",
                            node.target.lineno,
                            node.target.col_offset + len(node.target.id),
                        ),
                    )

        return injections

    def _apply_injections(  # noqa: C901, PLR0912, PLR0915
        self,
        tokens: list,
        injections: list[_Injection],
    ) -> list:
        """Inject type annotation tokens into the stream."""
        param_adds: set[tuple[int, int]] = set()
        param_replaces: set[tuple[int, int]] = set()
        var_adds: set[tuple[int, int]] = set()
        var_replaces: set[tuple[int, int]] = set()
        return_add_lines: set[int] = set()
        return_replace_pos: set[tuple[int, int]] = set()

        for inj in injections:
            pos = (inj.line, inj.col)
            match inj.kind:
                case "add_param":
                    param_adds.add(pos)
                case "replace_param":
                    param_replaces.add(pos)
                case "add_var":
                    var_adds.add(pos)
                case "replace_var":
                    var_replaces.add(pos)
                case "add_return":
                    return_add_lines.add(inj.line)
                case "replace_return":
                    return_replace_pos.add(pos)

        result: list = []
        i = 0
        n = len(tokens)

        while i < n:
            toknum, tokval, _start, end, _line = tokens[i]

            # after a NAME token, check if we should inject a parameter or
            # variable annotation
            if toknum == NAME:
                end_pos = (end[0], end[1])

                # add param annotation (no existing annotation)
                if end_pos in param_adds:
                    result.append((toknum, tokval))
                    typ = self._random_type()
                    result.append((OP, ":"))
                    result.append((NAME, f" {typ}"))
                    i += 1
                    continue

                # replace param annotation (has existing)
                if end_pos in param_replaces:
                    result.append((toknum, tokval))
                    i += 1
                    # skip the existing `:` and type expression
                    if i < n and tokens[i][0] == OP and tokens[i][1] == ":":
                        i = self._skip_type_expr(
                            tokens,
                            i + 1,
                            n,
                            {",", "=", ")"},
                        )
                    typ = self._random_type()
                    result.append((OP, ":"))
                    result.append((NAME, f" {typ}"))
                    continue

                # add var annotation
                if end_pos in var_adds:
                    result.append((toknum, tokval))
                    typ = self._random_type()
                    result.append((OP, ":"))
                    result.append((NAME, f" {typ}"))
                    i += 1
                    continue

                # replace var annotation
                if end_pos in var_replaces:
                    result.append((toknum, tokval))
                    i += 1
                    # skip existing `:` and type until `=`
                    if i < n and tokens[i][0] == OP and tokens[i][1] == ":":
                        i = self._skip_type_expr(
                            tokens,
                            i + 1,
                            n,
                            {"="},
                        )
                    typ = self._random_type()
                    result.append((OP, ":"))
                    result.append((NAME, f" {typ}"))
                    continue

            # return annotation, inject `->` type before the function body colon
            if (
                toknum == OP
                and tokval == ":"
                and self._is_func_body_colon(tokens, i, return_add_lines)
            ):
                typ = self._random_type()
                result.append((OP, "->"))
                result.append((NAME, f" {typ}"))
                result.append((toknum, tokval))
                i += 1
                continue

            # replace return annotation: `->` existing_type `:`
            if (
                toknum == OP
                and tokval == "->"
                and self._is_return_arrow(tokens, i, return_replace_pos)
            ):
                i += 1  # skip ->
                i = self._skip_type_expr(tokens, i, n, {":"})
                typ = self._random_type()
                result.append((OP, "->"))
                result.append((NAME, f" {typ}"))
                continue

            result.append((toknum, tokval))
            i += 1

        return result

    @classmethod
    def _skip_type_expr(
        cls,
        tokens: list,
        i: int,
        n: int,
        stops: set[str],
    ) -> int:
        """Advance past a type expression, respecting nesting."""
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
    def _is_func_body_colon(  # noqa: C901
        cls,
        tokens: list,
        idx: int,
        func_lines: set[int],
    ) -> bool:
        """Check if `:` at idx is a function definition body colon."""
        if not func_lines:
            return False
        tok_line = tokens[idx][2][0]
        if tok_line not in func_lines:
            j = idx - 1
            while j >= 0 and tokens[j][0] in cls.SKIP_TOKS:
                j -= 1
            if j >= 0 and tokens[j][0] == OP and tokens[j][1] == ")":
                depth = 1
                k = j - 1
                while k >= 0 and depth > 0:
                    if tokens[k][0] == OP and tokens[k][1] == ")":
                        depth += 1
                    elif tokens[k][0] == OP and tokens[k][1] == "(":
                        depth -= 1
                    k -= 1
                while k >= 0 and tokens[k][0] in cls.SKIP_TOKS:
                    k -= 1
                if k >= 0 and tokens[k][0] == NAME:
                    k -= 1
                    while k >= 0 and tokens[k][0] in cls.SKIP_TOKS:
                        k -= 1
                    if (
                        k >= 0
                        and tokens[k][0] == NAME
                        and tokens[k][1] in ("def", "async")
                        and tokens[k][2][0] in func_lines
                    ):
                        return True
            return False

        j = idx - 1
        while j >= 0 and tokens[j][0] in cls.SKIP_TOKS:
            j -= 1
        return j >= 0 and tokens[j][0] == OP and tokens[j][1] == ")"

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
