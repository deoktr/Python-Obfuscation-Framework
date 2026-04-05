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

DEFAULT_ARTIFACTS = [
    "/usr/bin/VBoxService",
    "/usr/bin/vmtoolsd",
    "/usr/bin/qemu-ga",
    "/proc/scsi/scsi",
]


class LinuxSandboxArtifactEvasion(BaseEvasion):
    CATEGORY = Category.SANDBOX
    PLATFORM = Platform.LINUX
    DESCRIPTION = "Detects known sandbox/VM artifact files on the filesystem"

    def __init__(self, artifacts: list[str] | None = None) -> None:
        self.artifacts = artifacts if artifacts is not None else DEFAULT_ARTIFACTS

    @staticmethod
    def import_tokens() -> list[tuple[int, str]]:
        return [
            (NAME, "import"),
            (NAME, "os"),
        ]

    def check_tokens(self) -> list[tuple[int, str]]:
        """Output.

        `any(os.path.exists(a) for a in ["/usr/bin/VBoxService",
        "/usr/bin/vmtoolsd", "/usr/bin/qemu-ga", "/proc/scsi/scsi"])`.
        """
        artifact_tokens: list[tuple[int, str]] = []
        for i, artifact in enumerate(self.artifacts):
            if i > 0:
                artifact_tokens.append((OP, ","))
            artifact_tokens.append((STRING, repr(artifact)))

        return [
            (NAME, "any"),
            (LPAR, "("),
            (NAME, "os"),
            (OP, "."),
            (NAME, "path"),
            (OP, "."),
            (NAME, "exists"),
            (LPAR, "("),
            (NAME, "a"),
            (RPAR, ")"),
            (NAME, "for"),
            (NAME, "a"),
            (NAME, "in"),
            (OP, "["),
            *artifact_tokens,
            (OP, "]"),
            (RPAR, ")"),
        ]
