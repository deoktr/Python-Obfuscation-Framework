from __future__ import annotations

import ast
import io
from tokenize import generate_tokens

from pof.utils.tokens import untokenize


def _simple_tokens() -> list[tuple[int, str]]:
    """Tokenize a simple valid program for use as evasion input."""
    source = 'print("hello")\n'
    tokens = list(generate_tokens(io.StringIO(source).readline))
    return [(tok.type, tok.string) for tok in tokens]


def test_evasion_syntax_valid(evasion_entry):
    """Verify that evasion output is syntactically valid Python."""
    name, cls, kwargs = evasion_entry

    evasion = cls(**kwargs)
    tokens = _simple_tokens()
    result_tokens = evasion.add_evasion(tokens)
    result = untokenize(result_tokens)

    try:
        ast.parse(result)
    except SyntaxError as exc:
        raise AssertionError(
            f"{name}: evasion output is not valid Python: {exc}\nOutput:\n{result}"
        ) from exc
