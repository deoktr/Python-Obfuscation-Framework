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

# ruff: noqa: F405, C901, PLR0912, PLR0915

import argparse
import sys
import time

from pof import Obfuscator, __version__
from pof.errors import PofError
from pof.evasion import *  # noqa: F403
from pof.logger import logger
from pof.obfuscator import *  # noqa: F403
from pof.stager import *  # noqa: F403
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


class PofCliFlagError(PofError):
    def __init__(self, flag) -> None:
        self.message = f"missing flag: {flag}"

    def __str__(self):
        return self.message


def add_obfuscation(tokens, args):
    if args.obf_string:
        logger.debug("obfuscating strings")
        tokens = StringsObfuscator(
            import_b64decode=True,
            import_b85decode=True,
        ).obfuscate_tokens(tokens)
    if args.obf_builtins:
        logger.debug("obfuscating builtins")
        tokens = BuiltinsObfuscator().obfuscate_tokens(tokens)
    if args.obf_deep_encryption:
        logger.debug("obfuscating deep_encryption")
        tokens = DeepEncryptionObfuscator().obfuscate_tokens(tokens)
    if args.obf_rc4:
        logger.debug("obfuscating rc4")
        tokens = RC4Obfuscator().obfuscate_tokens(tokens)
    if args.obf_shift:
        logger.debug("obfuscating shift")
        tokens = ShiftObfuscator().obfuscate_tokens(tokens)
    if args.obf_xor:
        logger.debug("obfuscating xor")
        tokens = XORObfuscator().obfuscate_tokens(tokens)
    if args.obf_bz2:
        logger.debug("obfuscating bz2")
        tokens = Bz2Obfuscator().obfuscate_tokens(tokens)
    if args.obf_gzip:
        logger.debug("obfuscating gzip")
        tokens = GzipObfuscator().obfuscate_tokens(tokens)
    if args.obf_lzma:
        logger.debug("obfuscating lzma")
        tokens = LzmaObfuscator().obfuscate_tokens(tokens)
    if args.obf_zlib:
        logger.debug("obfuscating zlib")
        tokens = ZlibObfuscator().obfuscate_tokens(tokens)
    if args.obf_constants:
        logger.debug("obfuscating constants")
        tokens = ConstantsObfuscator().obfuscate_tokens(tokens)
    if args.obf_a85:
        logger.debug("obfuscating a85")
        tokens = ASCII85Obfuscator().obfuscate_tokens(tokens)
    if args.obf_b16:
        logger.debug("obfuscating b16")
        tokens = Base16Obfuscator().obfuscate_tokens(tokens)
    if args.obf_b32:
        logger.debug("obfuscating b32")
        tokens = Base32Obfuscator().obfuscate_tokens(tokens)
    if args.obf_b32hex:
        logger.debug("obfuscating b32hex")
        tokens = Base32HexObfuscator().obfuscate_tokens(tokens)
    if args.obf_b64:
        logger.debug("obfuscating b64")
        tokens = Base64Obfuscator().obfuscate_tokens(tokens)
    if args.obf_b85:
        logger.debug("obfuscating b85")
        tokens = Base85Obfuscator().obfuscate_tokens(tokens)
    if args.obf_binascii:
        logger.debug("obfuscating binascii")
        tokens = BinasciiObfuscator().obfuscate_tokens(tokens)
    if args.obf_snt:
        logger.debug("obfuscating snt")
        tokens = SpacenTabObfuscator().obfuscate_tokens(tokens)
    if args.obf_whitespace:
        logger.debug("obfuscating whitespace")
        tokens = WhitespaceObfuscator().obfuscate_tokens(tokens)
    if args.obf_call:
        logger.debug("obfuscating call")
        tokens = CallObfuscator().obfuscate_tokens(tokens)
    if args.obf_doc:
        logger.debug("obfuscating doc")
        tokens = CharFromDocObfuscator().obfuscate_tokens(tokens)
    if args.obf_globals:
        logger.debug("obfuscating globals")
        tokens = GlobalsObfuscator().obfuscate_tokens(tokens)
    if args.obf_imports:
        logger.debug("obfuscating imports")
        tokens = ImportsObfuscator().obfuscate_tokens(tokens)
    if args.obf_extract_variables:
        logger.debug("obfuscating extract_variables")
        tokens = ExtractVariablesObfuscator().obfuscate_tokens(tokens)
    if args.obf_add_comments:
        logger.debug("obfuscating add_comments")
        tokens = AddCommentsObfuscator().obfuscate_tokens(tokens)
    if args.obf_add_newlines:
        logger.debug("obfuscating add_newlines")
        tokens = AddNewlinesObfuscator().obfuscate_tokens(tokens)
    if args.obf_names:
        logger.debug("obfuscating names")
        tokens = NamesObfuscator().obfuscate_tokens(tokens)
    if args.obf_numbers:
        logger.debug("obfuscating numbers")
        tokens = NumberObfuscator().obfuscate_tokens(tokens)
    if args.obf_tokens:
        logger.debug("obfuscating tokens")
        tokens = TokensObfuscator().obfuscate_tokens(tokens)
    if args.obf_comments:
        logger.debug("obfuscating comments")
        tokens = CommentsObfuscator().obfuscate_tokens(tokens)
    if args.obf_exceptions:
        logger.debug("obfuscating exceptions")
        tokens = ExceptionObfuscator().obfuscate_tokens(tokens)
    if args.obf_indents:
        logger.debug("obfuscating indents")
        tokens = IndentsObfuscator().obfuscate_tokens(tokens)
    if args.obf_logging:
        logger.debug("obfuscating logging")
        tokens = LoggingObfuscator().obfuscate_tokens(tokens)
    if args.obf_logging_remove:
        logger.debug("obfuscating logging remove")
        tokens = LoggingRemoveObfuscator().obfuscate_tokens(tokens)
    if args.obf_newline:
        logger.debug("obfuscating newline")
        tokens = NewlineObfuscator().obfuscate_tokens(tokens)
    if args.obf_print:
        logger.debug("obfuscating print")
        tokens = PrintObfuscator().obfuscate_tokens(tokens)
    if args.obf_docstrings:
        logger.debug("obfuscating docstrings")
        tokens = DocstringObfuscator().obfuscate_tokens(tokens)
    if args.obf_ipv6encoding:
        logger.debug("obfuscating ipv6encoding")
        tokens = IPv6Obfuscator().obfuscate_tokens(tokens)
    if args.obf_macencoding:
        logger.debug("obfuscating macencoding")
        tokens = MACObfuscator().obfuscate_tokens(tokens)
    if args.obf_uuidencoding:
        logger.debug("obfuscating uuidencoding")
        tokens = UUIDObfuscator().obfuscate_tokens(tokens)
    return tokens


def add_stagers(tokens, args):
    if args.stg_rc4:
        logger.debug("staging rc4")
        tokens = RC4Stager().generate_stager(tokens)
    if args.stg_download:
        logger.debug("staging download")
        tokens = DownloadStager().generate_stager(tokens)
    if args.stg_image:
        logger.debug("staging image")
        tokens = ImageStager().generate_stager(tokens)
    if args.stg_cl1pnet:
        logger.debug("staging cl1pnet")
        tokens = Cl1pNetStager().generate_stager(tokens)
    if args.stg_pastebin:
        logger.debug("staging pastebin")
        tokens = PastebinStager().generate_stager(tokens)
    if args.stg_pasters:
        logger.debug("staging pasters")
        tokens = PasteRsStager().generate_stager(tokens)
    if args.stg_quine:
        logger.debug("staging quine")
        tokens = QuineStager().generate_stager(tokens)
    return tokens


def add_evasion(tokens, args):
    if args.eva_argv:
        logger.debug("staging argv")
        tokens = ArgvEvasion(
            args.eva_argv_argv,
            args.eva_argv_position,
        ).add_evasion(tokens)
    if args.eva_cpu_count:
        logger.debug("staging cpu_count")
        tokens = CPUCountEvasion(args.eva_cpu_count_min).add_evasion(tokens)
    if args.eva_directory_exist:
        logger.debug("staging directory_exist")
        if args.eva_directory_exist_dir is None:
            flag = "--eva-directory-exist-dir"
            raise PofCliFlagError(flag)
        tokens = DirectoryExistEvasion(args.eva_directory_exist_dir).add_evasion(
            tokens,
        )
    if args.eva_directory_list_exist:
        logger.debug("staging directory_list_exist")
        # TODO (deoktr): split input list
        tokens = DirectoryListExistEvasion().add_evasion(tokens)
    if args.eva_directory_list_missing:
        logger.debug("staging directory_list_missing")
        # TODO (deoktr): split input list
        tokens = DirectoryListMissingEvasion().add_evasion(tokens)
    if args.eva_directory_missing:
        logger.debug("staging directory_missing")
        tokens = DirectoryMissingEvasion().add_evasion(tokens)
    if args.eva_exec_method:
        logger.debug("staging exec_method")
        tokens = ExecMethodEvasion().add_evasion(tokens)
    if args.eva_executable_path:
        logger.debug("staging executable_path")
        tokens = ExecPathEvasion().add_evasion(tokens)
    if args.eva_file_exist:
        logger.debug("staging file_exist")
        tokens = FileExistEvasion().add_evasion(tokens)
    if args.eva_file_list_exist:
        logger.debug("staging file_list_exist")
        tokens = FileListExistEvasion().add_evasion(tokens)
    if args.eva_file_list_missing:
        logger.debug("staging file_list_missing")
        tokens = FileListMissingEvasion().add_evasion(tokens)
    if args.eva_file_missing:
        logger.debug("staging file_missing")
        tokens = FileMissingEvasion().add_evasion(tokens)
    if args.eva_tmp:
        logger.debug("staging tmp")
        # TODO (deoktr): choose depending on target OS
        # LinuxTmpCountEvasion
        # TmpCountEvasion
        # WinTmpCountEvasion
        tokens = TmpCountEvasion(args.eva_tmp_count).add_evasion(tokens)
    if args.eva_ram_count:
        logger.debug("staging ram_count")
        tokens = LinuxRAMCountEvasion().add_evasion(tokens)
    if args.eva_debugger:
        logger.debug("staging debugger")
        tokens = DebuggerEvasion().add_evasion(tokens)
    if args.eva_tracemalloc:
        logger.debug("staging tracemalloc")
        tokens = TracemallocEvasion().add_evasion(tokens)
    if args.eva_prompt:
        logger.debug("staging prompt")
        tokens = WinPromptEvasion().add_evasion(tokens)
    if args.eva_multi:
        logger.debug("staging multi")
        tokens = MultiEvasion().add_evasion(tokens)
    if args.eva_domain:
        logger.debug("staging domain")
        tokens = DomainEvasion().add_evasion(tokens)
    if args.eva_hostname:
        logger.debug("staging hostname")
        tokens = HostnameEvasion().add_evasion(tokens)
    if args.eva_uid:
        logger.debug("staging uid")
        tokens = LinuxUIDEvasion().add_evasion(tokens)
    if args.eva_username:
        logger.debug("staging username")
        tokens = UsernameEvasion().add_evasion(tokens)
    if args.eva_proc_count:
        logger.debug("staging proc_count")
        tokens = LinuxProcCountEvasion().add_evasion(tokens)
    if args.eva_expire:
        logger.debug("staging expire")
        tokens = ExpireEvasion().add_evasion(tokens)
    if args.eva_uptime:
        logger.debug("staging uptime")
        tokens = LinuxUptimeEvasion().add_evasion(tokens)
    if args.eva_utc:
        logger.debug("staging utc")
        tokens = UTCEvasion().add_evasion(tokens)
    return tokens


class CLIObfuscator(Obfuscator):
    def run(self, source, args) -> str:
        """Execute a single obfuscator."""
        tokens = self._get_tokens(source)

        for _ in range(args.obf_count):
            tokens = add_obfuscation(tokens, args)

        tokens = add_stagers(tokens, args)
        tokens = add_evasion(tokens, args)

        if args.obf_result:
            for _ in range(args.obf_result_count):
                tokens = add_obfuscation(tokens, args)

        return self._untokenize(tokens)


def _handle(args) -> int:
    if args.version:
        print(__version__)  # noqa: T201
        return 0

    level = getattr(logging, args.logging)
    logger.setLevel(level)

    logger.info("starting obfuscation of %s", args.input.name)
    source = args.input.read()

    start = time.time()

    out = CLIObfuscator().run(source, args)

    end = time.time()

    if args.format_black:
        out = black_format(out)

    time_diff = round(end - start, 4)
    logger.info("took: %ds", time_diff)
    args.output.write(out)
    logger.info("successfully obfuscated %s to %s", args.input.name, args.output.name)
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
        help="raise exceptions instead of just logging them",
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
        "--logging",
        help="logging level, DEBUG, INFO, ERROR, CRITICAL",
        default="INFO",
    )

    # obfuscation
    parser.add_argument("--obf-string", action="store_true")
    parser.add_argument("--obf-builtins", action="store_true")
    parser.add_argument("--obf-deep_encryption", action="store_true")
    parser.add_argument("--obf-rc4", action="store_true")
    parser.add_argument("--obf-shift", action="store_true")
    parser.add_argument("--obf-xor", action="store_true")
    parser.add_argument("--obf-bz2", action="store_true")
    parser.add_argument("--obf-gzip", action="store_true")
    parser.add_argument("--obf-lzma", action="store_true")
    parser.add_argument("--obf-zlib", action="store_true")
    parser.add_argument("--obf-constants", action="store_true")
    parser.add_argument("--obf-definitions", action="store_true")
    parser.add_argument("--obf-a85", action="store_true")
    parser.add_argument("--obf-b16", action="store_true")
    parser.add_argument("--obf-b32", action="store_true")
    parser.add_argument("--obf-b32hex", action="store_true")
    parser.add_argument("--obf-b64", action="store_true")
    parser.add_argument("--obf-b85", action="store_true")
    parser.add_argument("--obf-binascii", action="store_true")
    parser.add_argument("--obf-snt", action="store_true")
    parser.add_argument("--obf-call", action="store_true")
    parser.add_argument("--obf-doc", action="store_true")
    parser.add_argument("--obf-globals", action="store_true")
    parser.add_argument("--obf-imports", action="store_true")
    parser.add_argument("--obf-extract_variables", action="store_true")
    parser.add_argument("--obf-add_comments", action="store_true")
    parser.add_argument("--obf-add_newlines", action="store_true")
    parser.add_argument("--obf-names", action="store_true")
    parser.add_argument("--obf-names_rope", action="store_true")
    parser.add_argument("--obf-numbers", action="store_true")
    parser.add_argument("--obf-tokens", action="store_true")
    parser.add_argument("--obf-comments", action="store_true")
    parser.add_argument("--obf-exceptions", action="store_true")
    parser.add_argument("--obf-indents", action="store_true")
    parser.add_argument("--obf-logging", action="store_true")
    parser.add_argument("--obf-logging-remove", action="store_true")
    parser.add_argument("--obf-newline", action="store_true")
    parser.add_argument("--obf-print", action="store_true")
    parser.add_argument("--obf-docstrings", action="store_true")
    parser.add_argument("--obf-ipv6encoding", action="store_true")
    parser.add_argument("--obf-macencoding", action="store_true")
    parser.add_argument("--obf-uuidencoding", action="store_true")

    # stager
    parser.add_argument("--stg-rc4", action="store_true")
    parser.add_argument("--stg-download", action="store_true")
    parser.add_argument("--stg-image", action="store_true")
    parser.add_argument("--stg-cl1pnet", action="store_true")
    parser.add_argument("--stg-pastebin", action="store_true")
    parser.add_argument("--stg-pasters", action="store_true")
    parser.add_argument("--stg-quine", action="store_true")

    # evasion
    parser.add_argument("--eva-argv", action="store_true")
    parser.add_argument("--eva-argv-argv", default="argv")
    parser.add_argument("--eva-argv-position", type=int, default=1)
    parser.add_argument("--eva-cpu-count", action="store_true")
    parser.add_argument("--eva-cpu-count-min", type=int, default=2)
    parser.add_argument("--eva-directory-exist", action="store_true")
    parser.add_argument("--eva-directory-exist-dir")
    parser.add_argument("--eva-directory-list-exist", action="store_true")
    parser.add_argument("--eva-directory-list-missing", action="store_true")
    parser.add_argument("--eva-directory-missing", action="store_true")
    parser.add_argument("--eva-exec-method", action="store_true")
    parser.add_argument("--eva-executable-path", action="store_true")
    parser.add_argument("--eva-file-exist", action="store_true")
    parser.add_argument("--eva-file-list-exist", action="store_true")
    parser.add_argument("--eva-file-list-missing", action="store_true")
    parser.add_argument("--eva-file-missing", action="store_true")
    parser.add_argument("--eva-tmp", action="store_true")
    parser.add_argument("--eva-tmp-count", type=int, default=5)
    parser.add_argument("--eva-ram-count", action="store_true")
    parser.add_argument("--eva-debugger", action="store_true")
    parser.add_argument("--eva-tracemalloc", action="store_true")
    parser.add_argument("--eva-prompt", action="store_true")
    parser.add_argument("--eva-multi", action="store_true")
    parser.add_argument("--eva-domain", action="store_true")
    parser.add_argument("--eva-hostname", action="store_true")
    parser.add_argument("--eva-uid", action="store_true")
    parser.add_argument("--eva-username", action="store_true")
    parser.add_argument("--eva-proc-count", action="store_true")
    parser.add_argument("--eva-expire", action="store_true")
    parser.add_argument("--eva-uptime", action="store_true")
    parser.add_argument("--eva-utc", action="store_true")

    # format
    parser.add_argument(
        "--format-black",
        action="store_true",
        help="format output with black",
    )

    # control
    parser.add_argument(
        "--obf-count",
        type=int,
        default=1,
        help="number of times the obfuscation is ran",
    )
    parser.add_argument(
        "--obf-result",
        action="store_true",
        help="run obfuscation a second time at the end, after the stager and evasion",
    )
    parser.add_argument(
        "--obf-result-count",
        type=int,
        default=1,
        help="number of times the obfuscation is ran at the end",
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
