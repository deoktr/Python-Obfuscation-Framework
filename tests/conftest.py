"""Root-level pytest plugin for random seed reproducibility."""

from __future__ import annotations

import random

import pytest


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--seed",
        type=int,
        default=None,
        help="base random seed for deterministic test runs",
    )


def pytest_configure(config: pytest.Config) -> None:
    seed = config.getoption("--seed", default=None)
    if seed is None:
        import os

        env_seed = os.environ.get("POF_SEED")
        if env_seed is not None:
            try:
                seed = int(env_seed)
            except ValueError:
                raise pytest.UsageError(
                    f"POF_SEED environment variable must be an integer, got: {env_seed!r}"
                ) from None
    if seed is None:
        seed = random.randrange(2**32)
    config._pof_base_seed = seed  # type: ignore[attr-defined]


def pytest_report_header(config: pytest.Config) -> str:
    return f"pof random seed: {config._pof_base_seed}"  # type: ignore[attr-defined]


def pytest_runtest_setup(item: pytest.Item) -> None:
    base_seed: int = item.config._pof_base_seed  # type: ignore[attr-defined]
    test_seed = (base_seed + hash(item.nodeid)) % (2**32)
    random.seed(test_seed)
    item._pof_seed = test_seed  # type: ignore[attr-defined]


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo) -> None:  # type: ignore[type-arg]
    outcome = yield
    report = outcome.get_result()
    if report.failed and call.when == "call":
        seed = getattr(item, "_pof_seed", None)
        if seed is not None:
            if report.longrepr:
                report.longreprtext += f"\n[pof] random seed: {seed}"


@pytest.fixture()
def pof_seed(request: pytest.FixtureRequest) -> int:
    """Return the per-test random seed."""
    return request.node._pof_seed  # type: ignore[attr-defined]
