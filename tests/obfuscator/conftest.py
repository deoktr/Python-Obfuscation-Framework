"""Obfuscator integration test configuration."""

from __future__ import annotations

import builtins
import io
import warnings
from base64 import b64decode
from dataclasses import dataclass, field
from pathlib import Path
from tokenize import generate_tokens
from typing import Any

import pytest
from pof.obfuscator import (
    AddCommentsObfuscator,
    AddNewlinesObfuscator,
    ASCII85Obfuscator,
    Base16Obfuscator,
    Base32HexObfuscator,
    Base32Obfuscator,
    Base64Obfuscator,
    Base85Obfuscator,
    BinasciiObfuscator,
    BooleanObfuscator,
    BuiltinsObfuscator,
    Bz2Obfuscator,
    CallObfuscator,
    CharFromDocObfuscator,
    CommentsObfuscator,
    ConstantsObfuscator,
    ControlFlowFlattenObfuscator,
    DeadCodeObfuscator,
    DeepEncryptionObfuscator,
    DocstringObfuscator,
    ExceptionObfuscator,
    ExtractVariablesObfuscator,
    GlobalsObfuscator,
    GzipObfuscator,
    ImportsObfuscator,
    IndentsObfuscator,
    IPv6Obfuscator,
    LoggingObfuscator,
    LoggingRemoveObfuscator,
    LzmaObfuscator,
    MACObfuscator,
    NamesObfuscator,
    NewlineObfuscator,
    NumberObfuscator,
    PrintObfuscator,
    RC4Obfuscator,
    ShiftObfuscator,
    SpacenTabObfuscator,
    StringsObfuscator,
    TokensObfuscator,
    UUIDObfuscator,
    WhitespaceObfuscator,
    XORObfuscator,
    ZlibObfuscator,
)
from pof.utils.tokens import untokenize

from .utils import exec_capture

FIXTURES_DIR = Path(__file__).parent / "fixtures"


@dataclass
class ObfuscatorEntry:
    class_ref: type
    name: str
    category: str
    is_output_preserving: bool = True
    constructor_args: dict[str, Any] = field(default_factory=dict)
    exec_globals: dict[str, Any] = field(default_factory=dict)
    xfail: bool = False
    xfail_reason: str = ""


@dataclass
class SourceFixture:
    name: str
    path: str
    expected_output: str


@dataclass
class SkipEntry:
    obfuscator_name: str
    fixture_name: str  # "*" means all fixtures
    reason: str


SKIP_LIST: list[SkipEntry] = []


OBFUSCATOR_REGISTRY: list[ObfuscatorEntry] = [
    # encoding
    ObfuscatorEntry(ASCII85Obfuscator, "ASCII85Obfuscator", "encoding"),
    ObfuscatorEntry(Base16Obfuscator, "Base16Obfuscator", "encoding"),
    ObfuscatorEntry(Base32Obfuscator, "Base32Obfuscator", "encoding"),
    ObfuscatorEntry(Base32HexObfuscator, "Base32HexObfuscator", "encoding"),
    ObfuscatorEntry(Base64Obfuscator, "Base64Obfuscator", "encoding"),
    ObfuscatorEntry(Base85Obfuscator, "Base85Obfuscator", "encoding"),
    ObfuscatorEntry(BinasciiObfuscator, "BinasciiObfuscator", "encoding"),
    ObfuscatorEntry(SpacenTabObfuscator, "SpacenTabObfuscator", "encoding"),
    ObfuscatorEntry(WhitespaceObfuscator, "WhitespaceObfuscator", "encoding"),
    # compression
    ObfuscatorEntry(Bz2Obfuscator, "Bz2Obfuscator", "compression"),
    ObfuscatorEntry(GzipObfuscator, "GzipObfuscator", "compression"),
    ObfuscatorEntry(LzmaObfuscator, "LzmaObfuscator", "compression"),
    ObfuscatorEntry(ZlibObfuscator, "ZlibObfuscator", "compression"),
    # cipher
    ObfuscatorEntry(
        XORObfuscator,
        "XORObfuscator",
        "cipher",
        exec_globals={"b64decode": b64decode},
    ),
    ObfuscatorEntry(RC4Obfuscator, "RC4Obfuscator", "cipher"),
    ObfuscatorEntry(ShiftObfuscator, "ShiftObfuscator", "cipher"),
    ObfuscatorEntry(
        DeepEncryptionObfuscator,
        "DeepEncryptionObfuscator",
        "cipher",
        constructor_args={"encryption_depth": 0},
    ),
    # esoteric
    ObfuscatorEntry(CallObfuscator, "CallObfuscator", "esoteric"),
    ObfuscatorEntry(CharFromDocObfuscator, "CharFromDocObfuscator", "esoteric"),
    ObfuscatorEntry(GlobalsObfuscator, "GlobalsObfuscator", "esoteric"),
    ObfuscatorEntry(ImportsObfuscator, "ImportsObfuscator", "esoteric"),
    # stegano
    ObfuscatorEntry(DocstringObfuscator, "DocstringObfuscator", "stegano"),
    ObfuscatorEntry(IPv6Obfuscator, "IPv6Obfuscator", "stegano"),
    ObfuscatorEntry(MACObfuscator, "MACObfuscator", "stegano"),
    ObfuscatorEntry(UUIDObfuscator, "UUIDObfuscator", "stegano"),
    # remove / behavior-altering
    ObfuscatorEntry(CommentsObfuscator, "CommentsObfuscator", "remove"),
    ObfuscatorEntry(
        ExceptionObfuscator,
        "ExceptionObfuscator",
        "remove",
        is_output_preserving=False,
    ),
    ObfuscatorEntry(IndentsObfuscator, "IndentsObfuscator", "remove"),
    ObfuscatorEntry(
        LoggingObfuscator,
        "LoggingObfuscator",
        "remove",
        is_output_preserving=False,
    ),
    ObfuscatorEntry(
        LoggingRemoveObfuscator,
        "LoggingRemoveObfuscator",
        "remove",
        is_output_preserving=False,
    ),
    ObfuscatorEntry(NewlineObfuscator, "NewlineObfuscator", "remove"),
    ObfuscatorEntry(
        PrintObfuscator,
        "PrintObfuscator",
        "remove",
        is_output_preserving=False,
    ),
    # Junk / behavior-altering
    ObfuscatorEntry(AddCommentsObfuscator, "AddCommentsObfuscator", "junk"),
    ObfuscatorEntry(AddNewlinesObfuscator, "AddNewlinesObfuscator", "junk"),
    ObfuscatorEntry(DeadCodeObfuscator, "DeadCodeObfuscator", "junk"),
    # name/variable obfuscators
    ObfuscatorEntry(ConstantsObfuscator, "ConstantsObfuscator", "other"),
    ObfuscatorEntry(
        NamesObfuscator,
        "NamesObfuscator",
        "other",
    ),
    ObfuscatorEntry(
        ExtractVariablesObfuscator,
        "ExtractVariablesObfuscator",
        "other",
    ),
    # value obfuscators
    ObfuscatorEntry(BooleanObfuscator, "BooleanObfuscator", "other"),
    ObfuscatorEntry(BuiltinsObfuscator, "BuiltinsObfuscator", "other"),
    ObfuscatorEntry(NumberObfuscator, "NumberObfuscator", "other"),
    ObfuscatorEntry(StringsObfuscator, "StringsObfuscator", "other"),
    ObfuscatorEntry(
        ControlFlowFlattenObfuscator,
        "ControlFlowFlattenObfuscator",
        "other",
    ),
    # other
    ObfuscatorEntry(TokensObfuscator, "TokensObfuscator", "other"),
]


def discover_fixtures() -> list[SourceFixture]:
    """Scan fixtures directory for .py files, execute each, and capture expected output."""
    fixtures: list[SourceFixture] = []
    for path in sorted(FIXTURES_DIR.glob("*.py"), key=lambda p: p.stem):
        if path.name == "__init__.py":
            continue
        try:
            source = path.read_text()
            expected_output = exec_capture(source, {"__builtins__": builtins})
        except Exception as exc:  # noqa: BLE001
            warnings.warn(
                f"Skipping fixture {path.name}: {exc}",
                stacklevel=1,
            )
            continue
        fixtures.append(
            SourceFixture(
                name=path.stem,
                path=str(path),
                expected_output=expected_output,
            )
        )
    return fixtures


FIXTURES: list[SourceFixture] = discover_fixtures()


def get_obfuscator_callable(
    entry: ObfuscatorEntry,
) -> Any:
    """Return a callable that accepts tokens and returns transformed tokens.

    Handles classmethod vs instance method dispatch.
    """
    instance = entry.class_ref(**entry.constructor_args)
    return instance.obfuscate_tokens


def run_obfuscation(entry: ObfuscatorEntry, source: str) -> str:
    """Tokenize source, apply obfuscator, untokenize, return result string."""
    io_obj = io.StringIO(source)
    tokens = list(generate_tokens(io_obj.readline))
    obfuscate = get_obfuscator_callable(entry)
    tokens = obfuscate(tokens)
    return untokenize(tokens)


def _should_skip(obfuscator_name: str, fixture_name: str) -> str | None:
    """Return skip reason if (obfuscator, fixture) is in SKIP_LIST, else None."""
    for entry in SKIP_LIST:
        if entry.obfuscator_name == obfuscator_name and (
            entry.fixture_name == "*" or entry.fixture_name == fixture_name
        ):
            return entry.reason
    return None


def load_fixture_source(fixture: SourceFixture) -> str:
    """Read fixture file contents."""
    with open(fixture.path) as f:
        return f.read()


def pytest_generate_tests(metafunc: pytest.Metafunc) -> None:
    """Dynamically parametrize tests over the obfuscator registry and fixtures."""
    if (
        "obfuscator_entry" in metafunc.fixturenames
        and "fixture_source" in metafunc.fixturenames
    ):
        combos = []
        ids = []
        for entry in OBFUSCATOR_REGISTRY:
            for fix in FIXTURES:
                skip_reason = _should_skip(entry.name, fix.name)
                if skip_reason:
                    continue
                combos.append((entry, fix))
                ids.append(f"{entry.name}-{fix.name}")
        metafunc.parametrize(
            "obfuscator_entry,fixture_source",
            combos,
            ids=ids,
        )
    elif "obfuscator_entry" in metafunc.fixturenames:
        metafunc.parametrize(
            "obfuscator_entry",
            OBFUSCATOR_REGISTRY,
            ids=[e.name for e in OBFUSCATOR_REGISTRY],
        )
    elif "fixture_source" in metafunc.fixturenames:
        metafunc.parametrize(
            "fixture_source",
            FIXTURES,
            ids=[f.name for f in FIXTURES],
        )


@pytest.fixture(autouse=True)
def _apply_xfail(request: pytest.FixtureRequest) -> None:
    """Automatically apply xfail markers for known-broken obfuscators."""
    entry = None
    if "obfuscator_entry" in request.fixturenames:
        # Access the parametrized value
        for mark in request.node.callspec.params.values():
            if isinstance(mark, ObfuscatorEntry) and mark.xfail:
                entry = mark
                break
    if entry is not None and entry.xfail:
        request.node.add_marker(
            pytest.mark.xfail(reason=entry.xfail_reason, strict=False)
        )
