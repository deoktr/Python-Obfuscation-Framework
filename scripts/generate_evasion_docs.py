#!/usr/bin/env python3
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

"""Generate Markdown documentation for all pof evasion techniques.

Usage:
    python3 scripts/generate_evasion_docs.py              # output to stdout
    python3 scripts/generate_evasion_docs.py -o docs.md   # output to file
"""

from __future__ import annotations

import argparse
import inspect
import io
import sys
import tokenize
from typing import Any

from pof import evasion
from pof.evasion.base import BaseEvasion, Category, Platform

SIMPLE_SOURCE = 'print("Hello, world!")\n'

# Example values by type annotation string
EXAMPLE_VALUES: dict[str, Any] = {
    "str": "example",
    "int": 2,
    "float": 2.0,
    "bool": True,
    "list": ["example"],
    "list[str]": ["example"],
    "datetime": None,  # skip datetime params
}


def get_example_value(param: inspect.Parameter) -> Any:
    """Get an example value for a constructor parameter."""
    if param.default is not inspect.Parameter.empty:
        return param.default

    annotation = param.annotation
    if annotation is inspect.Parameter.empty:
        return "example"

    type_str = str(annotation).replace("typing.", "").lower()
    for key, val in EXAMPLE_VALUES.items():
        if key in type_str:
            return val
    return "example"


def get_techniques() -> list[type[BaseEvasion]]:
    """Discover all BaseEvasion subclasses from pof.evasion."""
    techniques = []
    for name in sorted(evasion.__all__):
        if name in ("Category", "Platform", "MultiEvasion"):
            continue
        cls = getattr(evasion, name, None)
        if cls is None:
            continue
        if (
            isinstance(cls, type)
            and issubclass(cls, BaseEvasion)
            and cls is not BaseEvasion
        ):
            techniques.append(cls)
    return techniques


def get_params_table(cls: type[BaseEvasion]) -> str:
    """Extract constructor parameters and format as Markdown table."""
    try:
        sig = inspect.signature(cls.__init__)
    except (ValueError, TypeError):
        return "_No parameters_\n"

    params = []
    for name, param in sig.parameters.items():
        if name == "self":
            continue
        if name in ("invert", "failure_mode", "callback_name"):
            continue  # base class params, not technique-specific
        if param.kind in (
            inspect.Parameter.VAR_POSITIONAL,
            inspect.Parameter.VAR_KEYWORD,
        ):
            continue  # skip *args, **kwargs

        type_str = (
            str(param.annotation)
            .replace("typing.", "")
            .replace("<class '", "")
            .replace("'>", "")
            if param.annotation is not inspect.Parameter.empty
            else "-"
        )
        default_str = (
            repr(param.default)
            if param.default is not inspect.Parameter.empty
            else "_required_"
        )
        params.append((name, type_str, default_str))

    if not params:
        return "_No parameters_\n"

    lines = ["| Parameter | Type | Default |", "|---|---|---|"]
    for name, type_str, default_str in params:
        lines.append(f"| `{name}` | `{type_str}` | `{default_str}` |")
    return "\n".join(lines) + "\n"


def generate_example(cls: type[BaseEvasion]) -> str:
    """Generate example code by instantiating the technique with example values."""
    try:
        sig = inspect.signature(cls.__init__)
        kwargs = {}
        for name, param in sig.parameters.items():
            if name == "self":
                continue
            if name in ("invert", "failure_mode", "callback_name"):
                continue
            if param.kind in (
                inspect.Parameter.VAR_POSITIONAL,
                inspect.Parameter.VAR_KEYWORD,
            ):
                continue
            val = get_example_value(param)
            if val is None:
                continue
            kwargs[name] = val

        instance = cls(**kwargs)

        source_tokens = list(
            tokenize.generate_tokens(io.StringIO(SIMPLE_SOURCE).readline),
        )
        tokens = [(t.type, t.string) for t in source_tokens]
        result_tokens = instance.add_evasion(tokens)
        code = tokenize.untokenize(result_tokens)

        # Clean up formatting
        lines = code.strip().split("\n")
        if len(lines) > 20:  # noqa: PLR2004
            lines = [*lines[:18], "    # ... (truncated)", *lines[-2:]]
        return "\n".join(lines)
    except Exception as e:  # noqa: BLE001
        return f"# Example not available: {e}"


def generate_docs(techniques: list[type[BaseEvasion]]) -> str:
    """Generate full Markdown documentation."""
    output = []
    output.append("# Evasion Techniques Reference\n")
    output.append("_Auto-generated documentation. Do not edit manually._\n")
    output.append(f"**Total techniques**: {len(techniques)}\n")

    # Group by category
    categories: dict[str, list[type[BaseEvasion]]] = {}
    for cls in techniques:
        cat = getattr(cls, "CATEGORY", "uncategorized")
        cat_str = (
            cat.value if isinstance(cat, Category) else str(cat) or "uncategorized"
        )
        categories.setdefault(cat_str, []).append(cls)

    # Table of contents
    output.append("## Categories\n")
    for cat_name in sorted(categories.keys()):
        count = len(categories[cat_name])
        output.append(f"- [{cat_name.title()}](#{cat_name}) ({count} techniques)")
    output.append("")

    # Generate each category
    for cat_name in sorted(categories.keys()):
        cat_techniques = sorted(categories[cat_name], key=lambda c: c.__name__)
        output.append("---\n")
        output.append(f"## {cat_name.title()}\n")

        for cls in cat_techniques:
            name = cls.__name__
            platform = getattr(cls, "PLATFORM", "any")
            platform_str = (
                platform.value if isinstance(platform, Platform) else str(platform)
            )
            description = getattr(cls, "DESCRIPTION", "") or "No description provided"

            output.append(f"### `{name}`\n")
            output.append(f"- **Platform**: {platform_str}")
            output.append(f"- **Description**: {description}\n")

            # Parameters
            output.append("**Parameters**:\n")
            output.append(get_params_table(cls))

            # Example
            output.append("**Example output**:\n")
            example = generate_example(cls)
            output.append(f"```python\n{example}\n```\n")

    return "\n".join(output)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate Markdown documentation for pof evasion techniques.",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Output file path (default: stdout)",
        type=argparse.FileType("w"),
        default=sys.stdout,
    )
    args = parser.parse_args()

    techniques = get_techniques()
    docs = generate_docs(techniques)
    args.output.write(docs)

    if args.output is not sys.stdout:
        print(  # noqa: T201
            f"Generated documentation for {len(techniques)} techniques to {args.output.name}",  # noqa: E501
            file=sys.stderr,
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
