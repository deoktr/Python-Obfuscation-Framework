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

"""NamesObfuscator.

Renames user-defined function names, variables, and parameters while preserving
imports, builtins, keywords, class names, and class methods.
"""

from __future__ import annotations

import ast
import builtins as _builtins_mod
import io
import keyword
from tokenize import generate_tokens, untokenize

from pof.utils.generator import BasicGenerator


class _ScopeAnalyzer(ast.NodeVisitor):
    """Collect names that must NOT be renamed (imports, class methods, class names)."""

    def __init__(self) -> None:
        self.imported_names: set[str] = set()
        self.class_method_names: set[str] = set()
        self.class_names: set[str] = set()
        self._in_class: bool = False

    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            self.imported_names.add(alias.asname or alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        for alias in node.names:
            self.imported_names.add(alias.asname or alias.name)
        self.generic_visit(node)

    def visit_Assign(self, node: ast.Assign) -> None:
        """Detect `x = __import__(...)` and treat x as an imported name."""
        if len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            value = node.value
            # unwrap attribute chains: x = __import__("m", fromlist=["y"]).y
            # as they could be generated from the ImportObfuscator
            while isinstance(value, ast.Attribute):
                value = value.value
            if (
                isinstance(value, ast.Call)
                and isinstance(value.func, ast.Name)
                and value.func.id == "__import__"
            ):
                self.imported_names.add(node.targets[0].id)
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self.class_names.add(node.name)
        prev = self._in_class
        self._in_class = True
        self.generic_visit(node)
        self._in_class = prev

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        if self._in_class:
            self.class_method_names.add(node.name)
        prev = self._in_class
        self._in_class = False
        self.generic_visit(node)
        self._in_class = prev

    visit_AsyncFunctionDef = visit_FunctionDef  # noqa: N815


class _NameTransformer(ast.NodeTransformer):
    """Rename user-defined identifiers via a flat name mapping."""

    def __init__(
        self,
        skip: set[str],
        generator,
        imported_names: set[str] | None = None,
    ) -> None:
        self.skip = skip
        self.generator = generator
        self.mapping: dict[str, str] = {}
        self.imported_names = imported_names or set()

    def _get_new(self, name: str) -> str:
        if name not in self.mapping:
            new = next(self.generator)
            used = set(self.mapping.values())
            while new in self.skip or new in used:
                new = next(self.generator)
            self.mapping[name] = new
        return self.mapping[name]

    def _should_rename(self, name: str) -> bool:
        return name not in self.skip

    def visit_Name(self, node: ast.Name) -> ast.Name:
        if self._should_rename(node.id):
            node.id = self._get_new(node.id)
        return node

    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.FunctionDef:
        if self._should_rename(node.name):
            node.name = self._get_new(node.name)
        self.generic_visit(node)
        return node

    visit_AsyncFunctionDef = visit_FunctionDef  # noqa: N815

    def visit_ClassDef(self, node: ast.ClassDef) -> ast.ClassDef:
        self.generic_visit(node)
        return node

    def visit_arg(self, node: ast.arg) -> ast.arg:
        if self._should_rename(node.arg):
            node.arg = self._get_new(node.arg)
        return node

    def visit_Global(self, node: ast.Global) -> ast.Global:
        node.names = [
            self._get_new(n) if self._should_rename(n) else n for n in node.names
        ]
        return node

    def visit_Nonlocal(self, node: ast.Nonlocal) -> ast.Nonlocal:
        node.names = [
            self._get_new(n) if self._should_rename(n) else n for n in node.names
        ]
        return node

    def visit_keyword(self, node: ast.keyword) -> ast.keyword:
        # Only rename keyword args that match already-mapped parameter names
        if node.arg is not None and node.arg in self.mapping:
            node.arg = self.mapping[node.arg]
        self.generic_visit(node)
        return node

    def visit_ExceptHandler(self, node: ast.ExceptHandler) -> ast.ExceptHandler:
        if node.name is not None and self._should_rename(node.name):
            node.name = self._get_new(node.name)
        self.generic_visit(node)
        return node

    def _is_imported_root(self, node: ast.expr) -> bool:
        """Check if the root of an attribute chain is an imported name."""
        while isinstance(node, ast.Attribute):
            node = node.value
        if isinstance(node, ast.Name):
            return node.id in self.imported_names
        # Non-Name roots (Constant, Call, List, etc.) — conservatively skip
        return True

    def visit_Attribute(self, node: ast.Attribute) -> ast.Attribute:
        self.generic_visit(node)
        if node.attr in self.mapping and not self._is_imported_root(node.value):
            node.attr = self.mapping[node.attr]
        return node


class _StringFixer(ast.NodeTransformer):
    """Update string literals in getattr/setattr/delattr and __dict__ lookups."""

    def __init__(self, mapping: dict[str, str]) -> None:
        self.mapping = mapping

    def visit_Call(self, node: ast.Call) -> ast.Call:
        self.generic_visit(node)
        if (
            isinstance(node.func, ast.Name)
            and node.func.id in ("getattr", "setattr", "delattr")
            and len(node.args) >= 2  # noqa: PLR2004
            and isinstance(node.args[1], ast.Constant)
            and isinstance(node.args[1].value, str)
            and node.args[1].value in self.mapping
        ):
            node.args[1] = ast.Constant(value=self.mapping[node.args[1].value])
        return node

    def _is_globals_call(self, node: ast.expr) -> bool:
        """Check if node is a call to globals()."""
        return (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "globals"
            and not node.args
        )

    def visit_Subscript(self, node: ast.Subscript) -> ast.Subscript:
        self.generic_visit(node)
        if (
            isinstance(node.slice, ast.Constant)
            and isinstance(node.slice.value, str)
            and node.slice.value in self.mapping
            and (
                # __dict__['name'] pattern
                (
                    isinstance(node.value, ast.Attribute)
                    and node.value.attr == "__dict__"
                )
                # globals()['name'] pattern
                or self._is_globals_call(node.value)
            )
        ):
            node.slice = ast.Constant(value=self.mapping[node.slice.value])
        return node


class NamesObfuscator:
    """Obfuscate class/function/variables names."""

    BUILTINS = (
        "__file__",
        "__name__",
        "__doc__",
        "__builtins__",
        "__package__",
        "__loader__",
        "__spec__",
        "__build_class__",
        "__import__",
        "abs",
        "all",
        "any",
        "ascii",
        "bin",
        "breakpoint",
        "callable",
        "chr",
        "compile",
        "delattr",
        "dir",
        "divmod",
        "eval",
        "exec",
        "format",
        "getattr",
        "globals",
        "hasattr",
        "hash",
        "hex",
        "id",
        "input",
        "isinstance",
        "issubclass",
        "iter",
        "aiter",
        "len",
        "locals",
        "max",
        "min",
        "next",
        "anext",
        "oct",
        "ord",
        "pow",
        "print",
        "repr",
        "round",
        "setattr",
        "sorted",
        "sum",
        "vars",
        "None",
        "Ellipsis",
        "NotImplemented",
        "False",
        "True",
        "bool",
        "memoryview",
        "bytearray",
        "bytes",
        "classmethod",
        "complex",
        "dict",
        "enumerate",
        "filter",
        "float",
        "frozenset",
        "property",
        "int",
        "list",
        "map",
        "object",
        "range",
        "reversed",
        "set",
        "slice",
        "staticmethod",
        "str",
        "super",
        "tuple",
        "type",
        "zip",
        "__debug__",
        "BaseException",
        "Exception",
        "TypeError",
        "StopAsyncIteration",
        "StopIteration",
        "GeneratorExit",
        "SystemExit",
        "KeyboardInterrupt",
        "ImportError",
        "ModuleNotFoundError",
        "OSError",
        "EnvironmentError",
        "IOError",
        "EOFError",
        "RuntimeError",
        "RecursionError",
        "NotImplementedError",
        "NameError",
        "UnboundLocalError",
        "AttributeError",
        "SyntaxError",
        "IndentationError",
        "TabError",
        "LookupError",
        "IndexError",
        "KeyError",
        "ValueError",
        "UnicodeError",
        "UnicodeEncodeError",
        "UnicodeDecodeError",
        "UnicodeTranslateError",
        "AssertionError",
        "ArithmeticError",
        "FloatingPointError",
        "OverflowError",
        "ZeroDivisionError",
        "SystemError",
        "ReferenceError",
        "MemoryError",
        "BufferError",
        "Warning",
        "UserWarning",
        "EncodingWarning",
        "DeprecationWarning",
        "PendingDeprecationWarning",
        "SyntaxWarning",
        "RuntimeWarning",
        "FutureWarning",
        "ImportWarning",
        "UnicodeWarning",
        "BytesWarning",
        "ResourceWarning",
        "ConnectionError",
        "BlockingIOError",
        "BrokenPipeError",
        "ChildProcessError",
        "ConnectionAbortedError",
        "ConnectionRefusedError",
        "ConnectionResetError",
        "FileExistsError",
        "FileNotFoundError",
        "IsADirectoryError",
        "NotADirectoryError",
        "InterruptedError",
        "PermissionError",
        "ProcessLookupError",
        "TimeoutError",
        "open",
        "quit",
        "exit",
        "copyright",
        "credits",
        "license",
        "help",
    )

    RESERVED_WORDS = (
        "__init__",
        "__eq__",
        "__lt__",
        "append",  # on list
        "update",  # on dict
        "copy",  # copy dict or list
        "join",  # on string "".join()
        "decode",  # on string "".decode()
        "encode",  # on string "".encode()
        "__dict__",
        # TODO (deoktr): add all the others
        "quine",  # quine is used by pof to get the quine output
    )

    RESERVED = RESERVED_WORDS + BUILTINS + tuple(keyword.kwlist)
    KEYWORDS = tuple(keyword.kwlist)

    def __init__(self, generator=None) -> None:
        if generator is None:
            generator = BasicGenerator.alphabet_generator()
        self.generator = generator

    def obfuscate_tokens(self, tokens: list) -> list:
        """Obfuscate names in token list using AST analysis."""
        source = untokenize(tokens)
        tree = ast.parse(source)

        analyzer = _ScopeAnalyzer()
        analyzer.visit(tree)

        skip: set[str] = set(self.RESERVED)
        skip |= set(dir(_builtins_mod))
        skip |= analyzer.imported_names
        skip |= analyzer.class_method_names
        skip |= analyzer.class_names

        transformer = _NameTransformer(skip, self.generator, analyzer.imported_names)
        tree = transformer.visit(tree)
        ast.fix_missing_locations(tree)

        if transformer.mapping:
            fixer = _StringFixer(transformer.mapping)
            tree = fixer.visit(tree)
            ast.fix_missing_locations(tree)

        new_source = ast.unparse(tree)
        return list(generate_tokens(io.StringIO(new_source).readline))
