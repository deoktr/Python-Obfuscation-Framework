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
import io
import random
from tokenize import ENCODING, ENDMARKER, generate_tokens

from pof.utils.tokens import untokenize


class ControlFlowFlattenObfuscator:
    """Transform sequential function code into a state-machine dispatcher."""

    def __init__(self, min_statements: int = 3) -> None:
        self.min_statements = min_statements

    @staticmethod
    def _should_skip_function(body: list[ast.stmt]) -> bool:
        """Return True if the function body contains unsupported constructs."""
        for node in ast.walk(ast.Module(body=body, type_ignores=[])):
            if isinstance(
                node,
                (
                    ast.Yield,
                    ast.YieldFrom,
                    ast.AsyncFor,
                    ast.AsyncWith,
                    ast.Await,
                ),
            ):
                return True
        return False

    @staticmethod
    def _has_return(stmts: list[ast.stmt]) -> bool:
        """Check if any statement in the list is or contains a return."""
        for node in ast.walk(ast.Module(body=stmts, type_ignores=[])):
            if isinstance(node, ast.Return):
                return True
        return False

    @classmethod
    def _flatten_body(cls, body: list[ast.stmt]) -> list[ast.stmt]:
        """Transform a list of sequential statements into a state-machine dispatcher."""
        num_blocks = len(body)
        all_states = random.sample(range(100, 999), num_blocks + 1)
        exit_state = all_states[-1]
        block_states = all_states[:num_blocks]

        state_var = "_state"
        ret_var = "_ret"
        has_ret = cls._has_return(body)

        dispatcher_cases: list[ast.If | None] = []

        for idx, (state_num, stmt) in enumerate(zip(block_states, body, strict=True)):
            next_state = block_states[idx + 1] if idx + 1 < num_blocks else exit_state

            case_body: list[ast.stmt] = []

            if isinstance(stmt, ast.Return):
                # return value -> _ret = value; _state = exit
                if stmt.value is not None:
                    case_body.append(
                        ast.Assign(
                            targets=[ast.Name(id=ret_var, ctx=ast.Store())],
                            value=stmt.value,
                            lineno=0,
                        ),
                    )
                case_body.append(
                    ast.Assign(
                        targets=[ast.Name(id=state_var, ctx=ast.Store())],
                        value=ast.Constant(value=exit_state),
                        lineno=0,
                    ),
                )
            elif isinstance(stmt, ast.If):
                # if/else -> execute block, then set state based on which branch
                # for simplicity, keep the if/else inside the state block and
                # set next state after
                case_body.append(stmt)
                case_body.append(
                    ast.Assign(
                        targets=[ast.Name(id=state_var, ctx=ast.Store())],
                        value=ast.Constant(value=next_state),
                        lineno=0,
                    ),
                )
            else:
                case_body.append(stmt)
                case_body.append(
                    ast.Assign(
                        targets=[ast.Name(id=state_var, ctx=ast.Store())],
                        value=ast.Constant(value=next_state),
                        lineno=0,
                    ),
                )

            test = ast.Compare(
                left=ast.Name(id=state_var, ctx=ast.Load()),
                ops=[ast.Eq()],
                comparators=[ast.Constant(value=state_num)],
            )
            dispatcher_cases.append((test, case_body))

        if not dispatcher_cases:
            return body

        random.shuffle(dispatcher_cases)

        current: ast.stmt | None = None
        for test, case_body in reversed(dispatcher_cases):
            if current is None:
                current = ast.If(test=test, body=case_body, orelse=[])
            else:
                current = ast.If(test=test, body=case_body, orelse=[current])

        init_state = ast.Assign(
            targets=[ast.Name(id=state_var, ctx=ast.Store())],
            value=ast.Constant(value=block_states[0]),
            lineno=0,
        )

        init_ret: list[ast.stmt] = []
        if has_ret:
            init_ret.append(
                ast.Assign(
                    targets=[ast.Name(id=ret_var, ctx=ast.Store())],
                    value=ast.Constant(value=None),
                    lineno=0,
                ),
            )

        while_loop = ast.While(
            test=ast.Compare(
                left=ast.Name(id=state_var, ctx=ast.Load()),
                ops=[ast.NotEq()],
                comparators=[ast.Constant(value=exit_state)],
            ),
            body=[current],
            orelse=[],
        )

        result: list[ast.stmt] = [init_state, *init_ret, while_loop]

        if has_ret:
            result.append(ast.Return(value=ast.Name(id=ret_var, ctx=ast.Load())))

        return result

    def obfuscate_tokens(self, tokens: list) -> list:
        source = untokenize(tokens)

        try:
            tree = ast.parse(source)
        except SyntaxError:
            return tokens

        modified = False

        for node in ast.walk(tree):
            if not isinstance(node, ast.FunctionDef):
                continue

            body = node.body
            if len(body) < self.min_statements:
                continue

            if self._should_skip_function(body):
                continue

            node.body = self._flatten_body(body)
            modified = True

        if not modified:
            return tokens

        ast.fix_missing_locations(tree)
        new_source = ast.unparse(tree)

        try:
            new_tokens = list(generate_tokens(io.StringIO(new_source + "\n").readline))
        except Exception:  # noqa: BLE001
            return tokens

        # strip ENCODING and ENDMARKER
        result: list[tuple[int, str]] = []
        for toknum, tokval, *_ in new_tokens:
            if toknum in (ENCODING, ENDMARKER):
                continue
            result.append((toknum, tokval))

        return result
