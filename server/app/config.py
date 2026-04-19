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

# ruff: noqa: FBT003

import os


def env_bool(var, default=None):
    return os.environ.get(var, str(default)) in ["True", "true", "1"]


class Config:
    INPUT_SIZE_LIMIT = int(os.environ.get("INPUT_SIZE_LIMIT", str(200 * 1024)))
    ENABLE_BLACK_FORMAT = env_bool("ENABLE_BLACK_FORMAT", True)
    ENABLE_PYGMENT = env_bool("ENABLE_PYGMENT", True)


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True


config = {
    "production": ProductionConfig,
    "development": DevelopmentConfig,
    "default": ProductionConfig,
}
