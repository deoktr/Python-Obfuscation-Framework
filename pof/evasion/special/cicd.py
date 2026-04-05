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


class CICDEvasion(BaseEvasion):
    CATEGORY = Category.SPECIAL
    PLATFORM = Platform.ANY
    DESCRIPTION = "Detects CI/CD pipeline execution"

    @staticmethod
    def import_tokens():
        return [
            (NAME, "import"),
            (NAME, "os"),
        ]

    @staticmethod
    def check_tokens():
        """Output.

        `any(os.environ.get(v) is not None for v in [
            "GITHUB_ACTIONS", "GITLAB_CI", "JENKINS_URL", "CIRCLECI", "TRAVIS",
            "BUILDKITE", "TF_BUILD", "TEAMCITY_VERSION"])`.
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
            (STRING, '"GITHUB_ACTIONS"'),
            (OP, ","),
            (STRING, '"GITLAB_CI"'),
            (OP, ","),
            (STRING, '"JENKINS_URL"'),
            (OP, ","),
            (STRING, '"CIRCLECI"'),
            (OP, ","),
            (STRING, '"TRAVIS"'),
            (OP, ","),
            (STRING, '"BUILDKITE"'),
            (OP, ","),
            (STRING, '"TF_BUILD"'),
            (OP, ","),
            (STRING, '"TEAMCITY_VERSION"'),
            (OP, "]"),
            (RPAR, ")"),
        ]
