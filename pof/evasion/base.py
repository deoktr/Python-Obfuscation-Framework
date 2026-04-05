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

from enum import StrEnum
from tokenize import DEDENT, INDENT, LPAR, NAME, NEWLINE, OP, RPAR, STRING


class Platform(StrEnum):
    """Valid platform values for evasion techniques."""

    ANY = "any"
    LINUX = "linux"
    WINDOWS = "windows"
    DARWIN = "darwin"


class Category(StrEnum):
    """Valid category values for evasion techniques."""

    SANDBOX = "sandbox"
    GUARDRAILS = "guardrails"
    DEBUGGER = "debugger"
    SPECIAL = "special"


class BaseEvasion:
    # add evasion class name inside the exception
    ADD_CLASS_NAME: bool = True

    CATEGORY: str = ""
    PLATFORM: str = Platform.ANY
    DESCRIPTION: str = ""

    def __init_subclass__(cls, **kwargs: object) -> None:
        # validate PLATFORM and CATEGORY
        super().__init_subclass__(**kwargs)
        if "PLATFORM" in cls.__dict__:
            valid = {p.value for p in Platform}
            val = cls.__dict__["PLATFORM"]
            raw = val.value if isinstance(val, Platform) else val
            if raw not in valid:
                msg = (
                    f"{cls.__name__}.PLATFORM = {val!r} is invalid."
                    " Use Platform.{ANY,LINUX,WINDOWS,DARWIN}"
                )
                raise ValueError(msg)
        if "CATEGORY" in cls.__dict__:
            valid = {c.value for c in Category} | {""}
            val = cls.__dict__["CATEGORY"]
            raw = val.value if isinstance(val, Category) else val
            if raw not in valid:
                msg = (
                    f"{cls.__name__}.CATEGORY = {val!r} is invalid."
                    " Use Category.{SANDBOX,GUARDRAILS,DEBUGGER,SPECIAL}"
                )
                raise ValueError(msg)

    def fail_call_tokens(self) -> list[tuple[int, str]]:
        match getattr(self, "failure_mode", "exception"):
            case "exit":
                return [
                    (NAME, "import"),
                    (NAME, "sys"),
                    (NEWLINE, "\n"),
                    (NAME, "sys"),
                    (OP, "."),
                    (NAME, "exit"),
                    (LPAR, "("),
                    (RPAR, ")"),
                ]
            case "callback":
                name = getattr(self, "callback_name", None) or "evasion_callback"
                return [
                    (NAME, name),
                    (LPAR, "("),
                    (RPAR, ")"),
                ]
            case "return":
                return [
                    (NAME, "exit"),
                    (LPAR, "("),
                    (RPAR, ")"),
                ]
            case _:  # "exception" (default)
                return [
                    (NAME, "raise"),
                    (NAME, "Exception"),
                    (LPAR, "("),
                    (
                        STRING,
                        (
                            repr(self.__class__.__name__)
                            if self.ADD_CLASS_NAME
                            else repr("evasion check triggered")
                        ),
                    ),
                    (RPAR, ")"),
                ]

    @staticmethod
    def import_tokens() -> list[tuple[int, str]]:
        return []

    @staticmethod
    def check_tokens() -> list[tuple[int, str]]:
        return []

    def add_evasion(self, tokens):
        return [
            *self.import_tokens(),
            (NEWLINE, "\n"),
            (NAME, "if"),
            (LPAR, "("),
            *self.check_tokens(),
            (RPAR, ")"),
            (OP, ":"),
            (NEWLINE, "\n"),
            (INDENT, "    "),
            *self.fail_call_tokens(),
            (NEWLINE, "\n"),
            (DEDENT, ""),
            *tokens,
        ]
