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

import os
import random


def init_seed(seed: int | None = None) -> int:
    """Initialize the global random seed for deterministic obfuscation."""
    if seed is not None and not isinstance(seed, int):
        msg = f"seed must be an integer, got {type(seed).__name__}"
        raise TypeError(msg)
    if seed is None:
        env_seed = os.environ.get("POF_SEED")
        if env_seed is not None:
            try:
                seed = int(env_seed)
            except ValueError:
                msg = f"POF_SEED environment variable must be an integer, got: {env_seed!r}"  # noqa: E501
                raise ValueError(msg) from None
            random.seed(seed)
        else:
            seed = random.randrange(2**32)
            random.seed(seed)
    else:
        random.seed(seed)
    return seed
