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

from datetime import UTC, datetime, timedelta
from tokenize import LPAR, NAME, NUMBER, OP, RPAR

from pof.evasion.base import BaseEvasion, Category, Platform


class ExpireEvasion(BaseEvasion):
    CATEGORY = Category.GUARDRAILS
    PLATFORM = Platform.ANY
    DESCRIPTION = "Time-based expiration guardrail"

    def __init__(self, under_datetime=None) -> None:
        """Expire after a certain time (default 2 hours)."""
        if under_datetime is None:
            under_datetime = datetime.now(tz=UTC) + timedelta(hours=2)
        self.under_datetime = under_datetime

    @staticmethod
    def import_tokens():
        return [
            (NAME, "from"),
            (NAME, "datetime"),
            (NAME, "import"),
            (NAME, "datetime"),
        ]

    def check_tokens(self):
        """Time expiry check tokens.

        `datetime.now()>datetime(2023,1,2,1,1,1)`
        """
        return [
            (NAME, "datetime"),
            (OP, "."),
            (NAME, "now"),
            (LPAR, "("),
            (RPAR, ")"),
            (OP, ">"),
            (NAME, "datetime"),
            (LPAR, "("),
            (NUMBER, str(self.under_datetime.year)),
            (OP, ","),
            (NUMBER, str(self.under_datetime.month)),
            (OP, ","),
            (NUMBER, str(self.under_datetime.day)),
            (OP, ","),
            (NUMBER, str(self.under_datetime.hour)),
            (OP, ","),
            (NUMBER, str(self.under_datetime.minute)),
            (OP, ","),
            (NUMBER, str(self.under_datetime.second)),
            (RPAR, ")"),
        ]
