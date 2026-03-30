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

import argparse
import logging
import sys
import time

from pof import Obfuscator, __version__
from pof.errors import PofError
from pof.evasion import *  # noqa: F403
from pof.evasion import __all__ as all_evasion
from pof.logger import logger
from pof.obfuscator import *  # noqa: F403
from pof.obfuscator import __all__ as all_obfuscator
from pof.stager import *  # noqa: F403
from pof.stager import __all__ as all_stager
from pof.utils.format import black_format

handler = logging.StreamHandler()
formatter = logging.Formatter("%(levelname)s %(message)s\x1b[39m")

# colored logging
logging.addLevelName(logging.DEBUG, "\x1b[36m[*]")
logging.addLevelName(logging.INFO, "\x1b[32m[+]")
logging.addLevelName(logging.WARNING, "\x1b[33m[?]")
logging.addLevelName(logging.ERROR, "\x1b[31m[!]")
logging.addLevelName(logging.CRITICAL, "\x1b[31m[!!!]")

handler.setFormatter(formatter)

logging.basicConfig(level=logging.INFO, handlers=[handler])


class PofCliError(PofError):
    pass


class CLIObfuscator(Obfuscator):
    def obfuscator(self, source, obfuscator, *args, **kwargs) -> str:
        """Execute a single obfuscator."""
        tokens = self._get_tokens(source)

        try:
            if "Obfuscator" not in obfuscator:
                msg = "this is not an obfuscator"
                raise KeyError(msg)  # noqa: TRY301
            obf = globals()[obfuscator]
        except KeyError as err:
            lobf = ", ".join([e for e in all_obfuscator if "Obfuscator" in e])
            msg = f"obfuscator {obfuscator} not found in: {lobf}"
            raise PofCliError(msg) from err

        logger.info(f"using '{obf.__name__}' obfuscator")
        logger.debug(f"args={args}")
        logger.debug(f"kwargs={kwargs}")
        tokens = globals()[obfuscator](*args, **kwargs).obfuscate_tokens(tokens)
        return self._untokenize(tokens)

    def stager(self, source, stager, *args, **kwargs) -> str:
        """Execute a single stager."""
        tokens = self._get_tokens(source)

        try:
            if "Stager" not in stager:
                msg = "this is not a stager"
                raise KeyError(msg)  # noqa: TRY301
            obf = globals()[stager]
        except KeyError as err:
            lpl = ", ".join([e for e in all_stager if "Stager" in e])
            msg = f"stager '{stager}' not found in: {lpl}"
            raise PofCliError(msg) from err

        logger.info(f"using '{obf.__name__}' stager")
        logger.debug(f"{args=}")
        logger.debug(f"{kwargs=}")
        tokens = globals()[stager](*args, **kwargs).generate_stager(tokens)
        return self._untokenize(tokens)

    def evasion(self, source, evasion, *args, **kwargs) -> str:
        """Execute a single evasion method."""
        tokens = self._get_tokens(source)

        try:
            if "Evasion" not in evasion:
                msg = "this is not an evasion method"
                raise KeyError(msg)  # noqa: TRY301
            obf = globals()[evasion]
        except KeyError as err:
            lobf = ", ".join([e for e in all_evasion if "Evasion" in e])
            msg = f"evasion {evasion} not found in: {lobf}"
            raise PofCliError(msg) from err

        logger.info(f"using '{obf.__name__}' evasion")
        logger.debug(f"{args=}")
        logger.debug(f"{kwargs=}")
        tokens = globals()[evasion](*args, **kwargs).add_evasion(tokens)
        return self._untokenize(tokens)


def _handle(args) -> int:
    if args.version:
        print(__version__)  # noqa: T201
        return 0

    level = getattr(logging, args.logging)
    logger.setLevel(level)

    a = []
    k = {}
    if args.kwargs is not None:
        for e in args.kwargs:
            if "=" in e:
                key, value = e.split("=")
                k.update({key: value})
            else:
                a.append(e)

    logger.info(f"starting obfuscation of {args.input.name}")
    source = args.input.read()

    start = time.time()

    out = CLIObfuscator().__getattribute__(args.function)(source, *a, **k)

    end = time.time()

    if args.format:
        out = black_format(out)

    time_diff = round(end - start, 4)
    logger.info(f"took: {time_diff}s")
    args.output.write(out)
    logger.info(f"successfully obfuscated {args.input.name} to {args.output.name}")
    # no errors
    return 0


def _cli() -> int:
    parser = argparse.ArgumentParser(
        description="%(prog)s CLI tool to obfuscate Python source code.",
    )
    parser.add_argument("-v", "--version", action="store_true")
    parser.add_argument(
        "--raise-exceptions",
        action="store_true",
        help="raise exceptions instead of just logger them",
    )
    parser.add_argument(
        "input",
        nargs="?",  # required to be able to pipe to stdin
        help="input file",
        type=argparse.FileType("r"),
        default=sys.stdin,
    )
    parser.add_argument(
        "-o",
        "--output",
        help="output file",
        type=argparse.FileType("w"),
        default=sys.stdout,
    )
    parser.add_argument(
        "-f",
        "--function",
        help="obfuscation function, can be a specific function or preset: basic/moderate/advanced/extreme",
        default="moderate",
    )
    parser.add_argument(
        "--format",
        action="store_true",
        help="format output with black",
    )
    parser.add_argument(
        "--logging",
        help="logging level, DEBUG, INFO, ERROR, CRITICAL",
        default="INFO",
    )
    parser.add_argument(
        "-k",
        "--kwargs",
        help="variables for obfuscator",
        nargs="*",
    )

    args = parser.parse_args()

    try:
        return _handle(args)
    except Exception as e:
        logger.error(str(e))
        if args.raise_exceptions:
            raise
        logger.debug("use `--raise-exceptions` to see full trace back")
        return 1


if __name__ == "__main__":
    sys.exit(_cli())  # pragma: no cover
