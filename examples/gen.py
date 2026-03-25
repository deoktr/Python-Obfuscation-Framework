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

import pathlib
import random

import pof
from pof import BaseObfuscator
from pof.obfuscator import *
from pof.evasion import *
from pof.stager import *
from pof.utils.extract_names import NameExtract
from pof.utils.generator import AdvancedGenerator, BaseGenerator, BasicGenerator
from pof.utils.format import black_format


class Example(BaseObfuscator):
    def obfuscator(self, obfuscator_class, source):
        """Helper to apply a single obfuscator."""
        tokens = self._get_tokens(source)
        tokens = obfuscator_class.obfuscate_tokens(tokens)
        return self._untokenize(tokens)

    def stager(self, obfuscator_class, source):
        """Helper to apply a single stager."""
        tokens = self._get_tokens(source)
        tokens = obfuscator_class.generate_stager(tokens)
        return self._untokenize(tokens)

    def custom_complete(self, source: str):
        """Complete custom example obfuscation."""

        # tokenize Python source code
        tokens = self._get_tokens(source)

        # get all the names and add them to the RESERVED_WORDS for the generators
        reserved_words_add = NameExtract.get_names(tokens)
        BaseGenerator.extend_reserved(reserved_words_add)

        # remove comments
        tokens = CommentsObfuscator().obfuscate_tokens(tokens)

        # replace logging message with reversable random code
        tokens = LoggingObfuscator().obfuscate_tokens(tokens)

        # remove print statements
        # NOTE: in this example we want to print
        # tokens = PrintObfuscator().obfuscate_tokens(tokens)

        # replace exceptions with reversable random names
        tokens = ExceptionObfuscator(
            add_codes=True,
            generator=BasicGenerator.number_name_generator(),
        ).obfuscate_tokens(tokens)

        # configure global generator
        generator = AdvancedGenerator.multi_generator(
            {
                86: AdvancedGenerator.realistic_generator(),
                10: BasicGenerator.alphabet_generator(),
                4: BasicGenerator.number_name_generator(length=random.randint(2, 5)),
            }
        )

        # extract values and function to make them constant
        tokens = ConstantsObfuscator(
            generator=generator,
            obf_number_rate=0.7,
            obf_string_rate=0.1,
            obf_builtins_rate=0.3,
        ).obfuscate_tokens(tokens)

        # FIXME: broken for the moment
        # tokens = NamesObfuscator(generator=generator).obfuscate_tokens(tokens)

        # obfuscate function calls by calling `globals()` instead
        tokens = GlobalsObfuscator().obfuscate_tokens(tokens)

        # obfuscate builtins in many different ways
        tokens = BuiltinsObfuscator().obfuscate_tokens(tokens)

        b64decode_name = next(generator)
        b85decode_name = next(generator)
        string_obfuscator = StringsObfuscator(
            import_b64decode=True,
            import_b85decode=True,
            b64decode_name=b64decode_name,
            b85decode_name=b85decode_name,
        )

        # obfuscate strings in many different ways
        tokens = string_obfuscator.obfuscate_tokens(tokens)

        # for futur usage of `string_obfuscator` don't re-import base64 and 85
        string_obfuscator.import_b64decode = False
        string_obfuscator.import_b85decode = False

        # obfuscate numbers twice in a row in many different ways
        for _ in range(2):
            tokens = NumberObfuscator().obfuscate_tokens(tokens)

        # obfuscate builtins once again
        tokens = BuiltinsObfuscator().obfuscate_tokens(tokens)

        # obfuscate strings two more times
        for _ in range(2):
            tokens = string_obfuscator.obfuscate_tokens(tokens)

        # and produce Python source code from tokens
        return self._untokenize(tokens)

    def evasion_basic(self, source):
        """Basic example to use evasion."""
        tokens = self._get_tokens(source)

        tokens = FileMissingEvasion(file="/tmp/foobar").add_evasion(tokens)
        tokens = CPUCountEvasion(min_cpu_count=2).add_evasion(tokens)
        tokens = LinuxRAMCountEvasion(min_ram=2).add_evasion(tokens)
        tokens = TracemallocEvasion().add_evasion(tokens)

        from datetime import datetime, timedelta, timezone

        tokens = ExpireEvasion(datetime.now() + timedelta(hours=5)).add_evasion(tokens)

        tokens = DebuggerEvasion().add_evasion(tokens)

        return self._untokenize(tokens)


def obfuscate_to_file(out, file_name):
    file_name = file_name + ".py"
    file = pathlib.Path(__file__).parent / "out" / file_name
    with file.open("w") as f:
        f.write(out)


def run_all():
    file = pathlib.Path(__file__).parent / "source.py"
    with file.open() as f:
        source = f.read()

    # defaults from pof
    pof_obf = pof.Obfuscator()
    obfuscate_to_file(pof_obf.basic(source), "basic")
    obfuscate_to_file(pof_obf.obfuscate(source), "obfuscate")
    obfuscate_to_file(pof_obf.circles(source), "circles")

    # custom API example
    obf = Example()
    obfuscate_to_file(obf.custom_complete(source), "custom_complete")
    obfuscate_to_file(
        black_format(obf.custom_complete(source)), "custom_complete_format"
    )
    obfuscate_to_file(obf.evasion_basic(source), "evasion_basic")
    obfuscate_to_file(obf.obfuscator(VariablesObfuscator(), source), "variables_obf")
    obfuscate_to_file(obf.obfuscator(ConstantsObfuscator(), source), "constant_obf")
    obfuscate_to_file(
        obf.obfuscator(ExtractVariablesObfuscator(), source), "extractvariables_obf"
    )
    obfuscate_to_file(obf.obfuscator(BuiltinsObfuscator(), source), "buildtins_obf")
    obfuscate_to_file(obf.obfuscator(XORObfuscator(), source), "xor_obf")
    obfuscate_to_file(obf.obfuscator(RC4Obfuscator(), source), "rc4_obf")
    obfuscate_to_file(obf.obfuscator(SpacenTabObfuscator(), source), "snt_obf")
    obfuscate_to_file(obf.obfuscator(StringsObfuscator(), source), "strings_obf")
    obfuscate_to_file(obf.obfuscator(DocstringObfuscator(), source), "docstring_obf")
    obfuscate_to_file(obf.obfuscator(IndentsObfuscator(), source), "indent_obf")
    obfuscate_to_file(obf.obfuscator(TokensObfuscator(), source), "tokens_obf")
    obfuscate_to_file(obf.obfuscator(IPv6Obfuscator(), source), "ipv6_obf")
    obfuscate_to_file(obf.obfuscator(MACObfuscator(), source), "mac_obf")
    obfuscate_to_file(
        obf.obfuscator(DeepEncryptionObfuscator(), source), "deepencryption_obf"
    )
    obfuscate_to_file(obf.obfuscator(GlobalsObfuscator(), source), "globals_obf")
    obfuscate_to_file(obf.obfuscator(ControlFlowFlattenObfuscator(), source), "cff_obf")
    obfuscate_to_file(obf.stager(QuineStager(), source), "quine_stager")


if __name__ == "__main__":
    run_all()
