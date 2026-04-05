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

from tokenize import LPAR, NAME, OP, RPAR, STRING

from pof.evasion.base import BaseEvasion, Category, Platform


class ServerlessEvasion(BaseEvasion):
    CATEGORY = Category.SPECIAL
    PLATFORM = Platform.ANY
    DESCRIPTION = "Detects serverless/cloud function runtime"

    @staticmethod
    def import_tokens():
        return [
            (NAME, "import"),
            (NAME, "os"),
        ]

    @staticmethod
    def check_tokens():
        """Output.

        `any(os.environ.get(v) is not None for v in ["AWS_LAMBDA_FUNCTION_NAME",
        "FUNCTIONS_WORKER_RUNTIME", "K_SERVICE", "GOOGLE_CLOUD_PROJECT"])`.
        """
        return [
            (NAME, "any"),
            (LPAR, "("),
            (NAME, "os"),
            (OP, "."),
            (NAME, "environ"),
            (OP, "."),
            (NAME, "get"),
            (LPAR, "("),
            (NAME, "v"),
            (RPAR, ")"),
            (NAME, "is"),
            (NAME, "not"),
            (NAME, "None"),
            (NAME, "for"),
            (NAME, "v"),
            (NAME, "in"),
            (OP, "["),
            (STRING, '"AWS_LAMBDA_FUNCTION_NAME"'),
            (OP, ","),
            (STRING, '"FUNCTIONS_WORKER_RUNTIME"'),
            (OP, ","),
            (STRING, '"K_SERVICE"'),
            (OP, ","),
            (STRING, '"GOOGLE_CLOUD_PROJECT"'),
            (OP, "]"),
            (RPAR, ")"),
        ]
