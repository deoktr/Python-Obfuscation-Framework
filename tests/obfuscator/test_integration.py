"""Integration tests: every obfuscator x every source fixture.

Uses parametrization from conftest.py to generate test cases for all
obfuscator/fixture combinations. Two-tier assertion strategy:
  - Output-preserving: obfuscated code must produce identical stdout
  - Behavior-altering: obfuscated code must parse and execute without error
"""

from __future__ import annotations

import ast
import builtins

import pytest

from .conftest import (
    ObfuscatorEntry,
    SourceFixture,
    load_fixture_source,
    run_obfuscation,
)
from .utils import exec_capture


class TestOutputPreserving:
    """Round-trip tests for obfuscators that preserve stdout behavior."""

    def test_output_matches(
        self,
        obfuscator_entry: ObfuscatorEntry,
        fixture_source: SourceFixture,
    ) -> None:
        if not obfuscator_entry.is_output_preserving:
            return

        source = load_fixture_source(fixture_source)
        obfuscated = run_obfuscation(obfuscator_entry, source)

        # Verify obfuscated code is valid Python
        try:
            ast.parse(obfuscated)
        except SyntaxError as exc:
            pytest.fail(
                f"{obfuscator_entry.name} + {fixture_source.name}: "
                f"obfuscated output is not valid Python: {exc}"
            )

        # verify execution produces identical stdout, use a fresh globals dict
        # so the obfuscated code's own imports (base64, etc.) live in a clean
        # namespace with __builtins__
        exec_ns: dict = {"__builtins__": builtins}
        exec_ns.update(obfuscator_entry.exec_globals)
        captured = exec_capture(obfuscated, exec_ns)
        assert captured == fixture_source.expected_output, (
            f"{obfuscator_entry.name} + {fixture_source.name}: "
            f"stdout mismatch.\n"
            f"Expected:\n{fixture_source.expected_output!r}\n"
            f"Got:\n{captured!r}"
        )


class TestBehaviorAltering:
    """Syntactic validity tests for obfuscators that intentionally alter output."""

    def test_valid_and_executes(
        self,
        obfuscator_entry: ObfuscatorEntry,
        fixture_source: SourceFixture,
    ) -> None:
        if obfuscator_entry.is_output_preserving:
            return

        source = load_fixture_source(fixture_source)
        obfuscated = run_obfuscation(obfuscator_entry, source)

        # verify obfuscated code is valid Python
        try:
            ast.parse(obfuscated)
        except SyntaxError as exc:
            pytest.fail(
                f"{obfuscator_entry.name} + {fixture_source.name}: "
                f"obfuscated output is not valid Python: {exc}"
            )

        # verify execution completes without error
        try:
            exec_ns: dict = {"__builtins__": builtins}
            exec(obfuscated, exec_ns)  # noqa: S102
        except Exception as exc:  # noqa: BLE001
            pytest.fail(
                f"{obfuscator_entry.name} + {fixture_source.name}: "
                f"obfuscated code raised {type(exc).__name__}: {exc}"
            )
