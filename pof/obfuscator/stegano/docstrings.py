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

import ast
import random
from collections.abc import Iterator
from tokenize import (
    DEDENT,
    INDENT,
    LPAR,
    NAME,
    NEWLINE,
    OP,
    RPAR,
    STRING,
)

from pof.utils.encoding import Base64Encoding
from pof.utils.generator import BasicGenerator
from pof.utils.tokens import untokenize


class DocstringObfuscator:
    """Hide code inside doc strings."""

    # TODO (deoktr): add ability to choose entry point (function) name without calling
    # it put the exec code inside this function
    # TODO (deoktr): add ability to choose the base code
    # TODO (deoktr): add ability to split the docstring among multiple class/functions

    def __init__(
        self,
        encoding_class=None,
        generator: Iterator[str] | None = None,
        max_chunk_size: int = 200,
        min_chunk_size: int = 20,
    ) -> None:
        if encoding_class is None:
            encoding_class = Base64Encoding
        self.encoding_class = encoding_class

        if min_chunk_size > max_chunk_size:
            msg = f"min_chunk_size ({min_chunk_size}) must be <= max_chunk_size ({max_chunk_size})"  # noqa: E501
            raise ValueError(msg)

        self.min_chunk_size = min_chunk_size
        self.max_chunk_size = max_chunk_size

        if generator is None:
            generator = BasicGenerator.alphabet_generator()
        self.generator = generator

    def _split_into_chunks(
        self,
        encoded: str,
        min_chunk_size: int,
        max_chunk_size: int,
    ) -> list[str]:
        """Split an encoded string into variable-length chunks."""
        if max_chunk_size <= 0:
            return [encoded]

        chunks = []
        pos = 0
        total_length = len(encoded)

        while pos < total_length:
            remaining = total_length - pos
            if remaining <= max_chunk_size:
                chunks.append(encoded[pos:])
                break
            if min_chunk_size == max_chunk_size:
                chunk_size = max_chunk_size
            else:
                chunk_size = random.randint(min_chunk_size, max_chunk_size)
            actual_chunk_size = min(chunk_size, remaining)
            chunks.append(encoded[pos : pos + actual_chunk_size])
            pos += actual_chunk_size
        return chunks

    @staticmethod
    def _generate_container_tokens(
        name: str,
        chunk: str,
        is_class: bool,  # noqa: FBT001
    ) -> list[tuple]:
        """Generate tokens for a class or function definition with a docstring."""
        keyword = "class" if is_class else "def"
        params = [] if is_class else [(OP, "("), (OP, ")")]
        docstring = f'"""{chunk}"""'
        return [
            (NAME, keyword),
            (NAME, name),
            *params,
            (OP, ":"),
            (NEWLINE, "\n"),
            (INDENT, "    "),
            (STRING, docstring),
            (NEWLINE, "\n"),
            (NAME, "pass"),
            (NEWLINE, "\n"),
            (DEDENT, ""),
        ]

    def _get_exec_tokens(self, container_names: list[str]) -> list[tuple]:
        """Generate exec tokens that join all container docstrings and decode."""
        # build: "".join([C1.__doc__, C2.__doc__, ...]).replace('\n','')
        join_items = []
        for i, name in enumerate(container_names):
            if i > 0:
                join_items.append((OP, ","))
            join_items.extend(
                [
                    (NAME, name),
                    (OP, "."),
                    (NAME, "__doc__"),
                ],
            )

        docstring_tokens = [
            (STRING, '""'),
            (OP, "."),
            (NAME, "join"),
            (LPAR, "("),
            (OP, "["),
            *join_items,
            (OP, "]"),
            (RPAR, ")"),
            (OP, "."),
            (NAME, "replace"),
            (LPAR, "("),
            (STRING, repr(r"\n")),
            (OP, ","),
            (STRING, "''"),
            (RPAR, ")"),
        ]

        return [
            (NEWLINE, "\n"),
            (NAME, "exec"),
            (LPAR, "("),
            *self.encoding_class.decode_tokens(docstring_tokens),
            (RPAR, ")"),
        ]

    def obfuscate_tokens(self, tokens: list[tuple]) -> list[tuple]:
        code = untokenize(tokens)

        encoded = ast.literal_eval(
            untokenize(self.encoding_class.encode_tokens(code.encode())),
        )

        chunks = self._split_into_chunks(
            encoded,
            self.min_chunk_size,
            self.max_chunk_size,
        )

        container_names = []
        container_names.extend(next(self.generator) for _ in chunks)

        result = [
            *self.encoding_class.import_tokens(),
            (NEWLINE, "\n"),
        ]

        for name, chunk in zip(container_names, chunks, strict=True):
            is_class = random.choice([True, False])
            result.extend(self._generate_container_tokens(name, chunk, is_class))

        result.extend(self._get_exec_tokens(container_names))
        result.append((NEWLINE, "\n"))
        return result
