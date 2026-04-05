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

"""pof (Python Obfuscator Framework)."""

import io
import random
from tokenize import generate_tokens

from pof.obfuscator import (
    AddCommentsObfuscator,
    AddTypeHintsObfuscator,
    BooleanObfuscator,
    BuiltinsObfuscator,
    CommentsObfuscator,
    ConstantsObfuscator,
    DeadCodeObfuscator,
    DocstringObfuscator,
    ExceptionObfuscator,
    GlobalsObfuscator,
    IndentsObfuscator,
    LoggingObfuscator,
    NamesObfuscator,
    NewlineObfuscator,
    NumberObfuscator,
    StringsObfuscator,
    TypeHintsObfuscator,
)
from pof.utils.extract_names import NameExtract
from pof.utils.generator import AdvancedGenerator, BaseGenerator, BasicGenerator
from pof.utils.tokens import untokenize


class BaseObfuscator:
    @staticmethod
    def _get_tokens(source: str):
        # TODO (deoktr): this is not safe, the \r could be inside a string, probably
        # should get tokens first, and update all the instances of newline
        if "\r" in source:
            source = source.replace("\r\n", "\n").replace("\r", "\n")
        if not source.endswith("\n"):
            source += "\n"
        io_obj = io.StringIO(source)
        return list(generate_tokens(io_obj.readline))

    @staticmethod
    def _untokenize(tokens):
        return untokenize(tokens)


class Obfuscator(BaseObfuscator):
    def basic(self, source):
        """Just the bare minimum obfuscation."""
        tokens = self._get_tokens(source)
        tokens = CommentsObfuscator().obfuscate_tokens(tokens)
        generator = BasicGenerator.alphabet_generator()
        tokens = NamesObfuscator(generator=generator).obfuscate_tokens(tokens)
        return self._untokenize(tokens)

    def moderate(self, source):
        tokens = self._get_tokens(source)
        tokens = CommentsObfuscator().obfuscate_tokens(tokens)
        tokens = TypeHintsObfuscator().obfuscate_tokens(tokens)
        generator = BasicGenerator.alphabet_generator()
        tokens = NamesObfuscator(generator=generator).obfuscate_tokens(tokens)
        tokens = NumberObfuscator().obfuscate_tokens(tokens)
        tokens = BooleanObfuscator().obfuscate_tokens(tokens)
        tokens = StringsObfuscator().obfuscate_tokens(tokens)
        tokens = IndentsObfuscator().obfuscate_tokens(tokens)
        tokens = NewlineObfuscator().obfuscate_tokens(tokens)
        return self._untokenize(tokens)

    def advanced(self, source):
        tokens = self._get_tokens(source)

        # do not generate any names that was present in source
        reserved_words_add = NameExtract.get_names(tokens)
        BaseGenerator.extend_reserved(reserved_words_add)

        tokens = CommentsObfuscator().obfuscate_tokens(tokens)
        tokens = TypeHintsObfuscator().obfuscate_tokens(tokens)

        generator = AdvancedGenerator.multi_generator(
            {
                86: AdvancedGenerator.realistic_generator(),
                10: BasicGenerator.alphabet_generator(),
                4: BasicGenerator.number_name_generator(length=random.randint(2, 5)),
            },
        )

        tokens = DeadCodeObfuscator(generator=generator).obfuscate_tokens(tokens)
        tokens = AddTypeHintsObfuscator().obfuscate_tokens(tokens)
        tokens = NamesObfuscator(generator=generator).obfuscate_tokens(tokens)
        tokens = NumberObfuscator().obfuscate_tokens(tokens)
        tokens = BooleanObfuscator().obfuscate_tokens(tokens)
        tokens = StringsObfuscator().obfuscate_tokens(tokens)
        tokens = IndentsObfuscator().obfuscate_tokens(tokens)
        tokens = NewlineObfuscator().obfuscate_tokens(tokens)
        return self._untokenize(tokens)

    def extreme(self, source):
        """Complete chained obfuscation."""
        tokens = self._get_tokens(source)

        # do not generate any names that was present in source
        reserved_words_add = NameExtract.get_names(tokens)
        BaseGenerator.extend_reserved(reserved_words_add)

        # clean input
        tokens = CommentsObfuscator().obfuscate_tokens(tokens)
        tokens = TypeHintsObfuscator().obfuscate_tokens(tokens)

        # configure generator
        generator = AdvancedGenerator.multi_generator(
            {
                86: AdvancedGenerator.realistic_generator(),
                10: BasicGenerator.alphabet_generator(),
                4: BasicGenerator.number_name_generator(length=random.randint(2, 5)),
            },
        )

        # add trash
        tokens = DeadCodeObfuscator(
            max_function_depth=3,
            max_branches=5,
            generate_classes=True,
            generator=generator,
        ).obfuscate_tokens(tokens)
        tokens = AddTypeHintsObfuscator().obfuscate_tokens(tokens)

        # core obfuscation
        tokens = ConstantsObfuscator(
            generator=generator,
            obf_number_rate=0.7,
            # obf_string_rate=0.1,
            obf_string_rate=0,  # FIXME (deoktr): when string obfuscation is enable and
            # name obfuscator comes next, the time delai of
            # http requests are very slow, idk why
            obf_builtins_rate=0.3,
        ).obfuscate_tokens(tokens)

        tokens = NamesObfuscator(generator=generator).obfuscate_tokens(tokens)

        tokens = GlobalsObfuscator().obfuscate_tokens(tokens)
        tokens = BuiltinsObfuscator().obfuscate_tokens(tokens)

        b64decode_name = next(generator)
        b85decode_name = next(generator)
        string_obfuscator = StringsObfuscator(
            import_b64decode=True,
            import_b85decode=True,
            b64decode_name=b64decode_name,
            b85decode_name=b85decode_name,
        )
        tokens = string_obfuscator.obfuscate_tokens(tokens)
        string_obfuscator.import_b64decode = False
        string_obfuscator.import_b85decode = False

        for _ in range(2):
            tokens = NumberObfuscator().obfuscate_tokens(tokens)
            tokens = string_obfuscator.obfuscate_tokens(tokens)
            tokens = BooleanObfuscator().obfuscate_tokens(tokens)

        tokens = AddCommentsObfuscator().obfuscate_tokens(tokens)

        # clean output
        tokens = IndentsObfuscator().obfuscate_tokens(tokens)
        tokens = NewlineObfuscator().obfuscate_tokens(tokens)

        return self._untokenize(tokens)

    def circles(self, source):
        tokens = self._get_tokens(source)
        generator = AdvancedGenerator.fixed_length_generator()
        tokens = CommentsObfuscator().obfuscate_tokens(tokens)
        tokens = ExceptionObfuscator(generator=generator).obfuscate_tokens(tokens)
        tokens = LoggingObfuscator(generator=generator).obfuscate_tokens(tokens)
        tokens = NamesObfuscator(generator=generator).obfuscate_tokens(tokens)
        tokens = ConstantsObfuscator(
            generator=generator,
            obf_number_rate=1,
            obf_string_rate=1,
            obf_builtins_rate=1,
        ).obfuscate_tokens(tokens)
        tokens = IndentsObfuscator().obfuscate_tokens(tokens)
        tokens = NewlineObfuscator().obfuscate_tokens(tokens)
        return self._untokenize(tokens)

    def docstring(self, source):
        tokens = self._get_tokens(source)
        tokens = DocstringObfuscator().obfuscate_tokens(tokens)
        generator = BasicGenerator.alphabet_generator()
        tokens = NamesObfuscator(generator=generator).obfuscate_tokens(tokens)
        tokens = BuiltinsObfuscator().obfuscate_tokens(tokens)
        tokens = StringsObfuscator(
            import_b64decode=True,
            import_b85decode=True,
        ).obfuscate_tokens(tokens)
        return self._untokenize(tokens)
