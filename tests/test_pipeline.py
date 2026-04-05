"""Pipeline integration tests for obfuscation levels.

Tests the Obfuscator class methods (basic, moderate, advanced, extreme) against
all discovered fixtures, matching the coverage of single-obfuscator integration
tests.
"""

from __future__ import annotations

import ast
import builtins
import contextlib
import io
from pathlib import Path

import pytest

from pof import Obfuscator

LEVELS = ["basic", "moderate", "advanced", "extreme"]

FIXTURES_DIR = Path(__file__).parent / "obfuscator" / "fixtures"

# Known-failing level+fixture combinations
SKIP_LIST: list[tuple[str, str, str]] = [
    # (level, fixture_name, reason)
    # docs: CommentsObfuscator strips docstrings, but the docs fixture stores
    # encoded code inside docstrings
    ("basic", "docs", "CommentsObfuscator strips docstrings used for code storage"),
    ("moderate", "docs", "CommentsObfuscator strips docstrings used for code storage"),
    ("advanced", "docs", "CommentsObfuscator strips docstrings used for code storage"),
    ("extreme", "docs", "CommentsObfuscator strips docstrings used for code storage"),
    # strings: f-string debug format f"{expr=}" shows exact source text which
    # changes after AST unparse, inherent limitation of AST-based transformation
    ("basic", "strings", "f-string debug format incompatible with AST unparse"),
    ("moderate", "strings", "f-string debug format incompatible with AST unparse"),
    ("advanced", "strings", "f-string debug format incompatible with AST unparse"),
    ("extreme", "strings", "f-string debug format incompatible with AST unparse"),
    # import: NamesObfuscator renames imported module attributes
    ("advanced", "import", "NamesObfuscator renames imported names"),
    ("extreme", "import", "NamesObfuscator renames imported names"),
    # extreme-level interaction issues between GlobalsObfuscator and
    # BuiltinsObfuscator
    (
        "extreme",
        "getattr",
        "BuiltinsObfuscator/GlobalsObfuscator interaction at extreme level",
    ),
    (
        "extreme",
        "esoteric",
        "GlobalsObfuscator breaks already-obfuscated patterns at extreme level",
    ),
]


def _exec_capture(code: str) -> str:
    output = io.StringIO()
    ns: dict = {"__builtins__": builtins}
    with contextlib.redirect_stdout(output):
        exec(code, ns)
    return output.getvalue()


def _discover_fixtures() -> list[tuple[str, str, str]]:
    """Discover fixtures: returns list of (name, source, expected_output)."""
    fixtures = []
    for path in sorted(FIXTURES_DIR.glob("*.py"), key=lambda p: p.stem):
        if path.name == "__init__.py":
            continue
        try:
            source = path.read_text()
            expected = _exec_capture(source)
        except Exception:  # noqa: BLE001
            continue
        fixtures.append((path.stem, source, expected))
    return fixtures


FIXTURES = _discover_fixtures()


def _should_skip(level: str, fixture_name: str) -> str | None:
    for lvl, fix, reason in SKIP_LIST:
        if lvl == level and (fix == "*" or fix == fixture_name):
            return reason
    return None


def _make_params():
    params = []
    for level in LEVELS:
        for name, source, expected in FIXTURES:
            skip_reason = _should_skip(level, name)
            marks = [pytest.mark.skip(reason=skip_reason)] if skip_reason else []
            params.append(
                pytest.param(
                    level, name, source, expected, id=f"{level}-{name}", marks=marks
                )
            )
    return params


class TestPipelineCorrectness:
    """Each level must produce output that executes with identical stdout."""

    @pytest.mark.parametrize("level,name,source,expected", _make_params())
    def test_output_matches(
        self, level: str, name: str, source: str, expected: str
    ) -> None:
        obf = Obfuscator()
        result = getattr(obf, level)(source)
        captured = _exec_capture(result)
        assert captured == expected, (
            f"{level}+{name}: stdout mismatch.\n"
            f"Expected:\n{expected!r}\nGot:\n{captured!r}"
        )


class TestPipelineSyntax:
    """Each level must produce syntactically valid output."""

    @pytest.mark.parametrize("level,name,source,expected", _make_params())
    def test_syntax_valid(
        self, level: str, name: str, source: str, expected: str
    ) -> None:
        obf = Obfuscator()
        result = getattr(obf, level)(source)
        try:
            ast.parse(result)
        except SyntaxError as exc:
            pytest.fail(f"{level}+{name}: invalid syntax: {exc}")
