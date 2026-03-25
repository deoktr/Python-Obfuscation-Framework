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

from .boolean import BooleanObfuscator
from .builtins import BuiltinsObfuscator
from .cipher.deep_encryption import DeepEncryptionObfuscator
from .cipher.rc4 import RC4Obfuscator
from .cipher.shift import ShiftObfuscator
from .cipher.xor import XORObfuscator
from .compression.bz2 import Bz2Obfuscator
from .compression.gzip import GzipObfuscator
from .compression.lzma import LzmaObfuscator
from .compression.zlib import ZlibObfuscator
from .constants import ConstantsObfuscator
from .controlflow.control_flow_flatten import ControlFlowFlattenObfuscator
from .definitions import DefinitionsObfuscator
from .encoding.a85 import ASCII85Obfuscator
from .encoding.b16 import Base16Obfuscator
from .encoding.b32 import Base32Obfuscator
from .encoding.b32hex import Base32HexObfuscator
from .encoding.b64 import Base64Obfuscator
from .encoding.b85 import Base85Obfuscator
from .encoding.binascii import BinasciiObfuscator
from .encoding.snt import SpacenTabObfuscator
from .encoding.whitespace import WhitespaceObfuscator
from .esoteric.call import CallObfuscator
from .esoteric.doc import CharFromDocObfuscator
from .esoteric.globals import GlobalsObfuscator
from .esoteric.imports import ImportsObfuscator
from .extract_variables import ExtractVariablesObfuscator
from .junk.add_comments import AddCommentsObfuscator
from .junk.add_newlines import AddNewlinesObfuscator
from .names import NamesObfuscator
from .names_rope import NamesRopeObfuscator
from .numbers import NumberObfuscator
from .other.tokens import TokensObfuscator
from .remove.comments import CommentsObfuscator
from .remove.exceptions import ExceptionObfuscator
from .remove.indents import IndentsObfuscator
from .remove.loggings import LoggingObfuscator, LoggingRemoveObfuscator
from .remove.newline import NewlineObfuscator
from .remove.print import PrintObfuscator
from .stegano.docstrings import DocstringObfuscator
from .stegano.ipv6encoding import IPv6Obfuscator
from .stegano.macencoding import MACObfuscator
from .stegano.uuidencoding import UUIDObfuscator
from .strings import StringsObfuscator
from .variables import VariablesObfuscator

__all__ = [
    "ASCII85Obfuscator",
    "AddCommentsObfuscator",
    "AddNewlinesObfuscator",
    "Base16Obfuscator",
    "Base32HexObfuscator",
    "Base32Obfuscator",
    "Base64Obfuscator",
    "Base85Obfuscator",
    "BinasciiObfuscator",
    "BooleanObfuscator",
    "BuiltinsObfuscator",
    "Bz2Obfuscator",
    "CallObfuscator",
    "CharFromDocObfuscator",
    "CommentsObfuscator",
    "ConstantsObfuscator",
    "ControlFlowFlattenObfuscator",
    "DeepEncryptionObfuscator",
    "DefinitionsObfuscator",
    "DocstringObfuscator",
    "ExceptionObfuscator",
    "ExtractVariablesObfuscator",
    "GlobalsObfuscator",
    "GzipObfuscator",
    "IPv6Obfuscator",
    "ImportsObfuscator",
    "IndentsObfuscator",
    "LoggingObfuscator",
    "LoggingRemoveObfuscator",
    "LzmaObfuscator",
    "MACObfuscator",
    "NamesObfuscator",
    "NamesRopeObfuscator",
    "NewlineObfuscator",
    "NumberObfuscator",
    "PrintObfuscator",
    "RC4Obfuscator",
    "ShiftObfuscator",
    "SpacenTabObfuscator",
    "StringsObfuscator",
    "TokensObfuscator",
    "UUIDObfuscator",
    "VariablesObfuscator",
    "WhitespaceObfuscator",
    "XORObfuscator",
    "ZlibObfuscator",
]
