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

from .debugger.breakpoint_hook import BreakpointHookEvasion
from .debugger.coverage import CoverageEvasion
from .debugger.cprofile import CProfileEvasion
from .debugger.debugger import DebuggerEvasion
from .debugger.linux_debug_process import LinuxDebugProcessEvasion
from .debugger.macos_debug_process import MacDebugProcessEvasion
from .debugger.tracemalloc_evasion import TracemallocEvasion
from .debugger.win_debug_process import WinDebugProcessEvasion
from .debugger.win_debugger import WinDebuggerEvasion
from .guardrails.argv import ArgvEvasion
from .guardrails.directory_exist import DirectoryExistEvasion
from .guardrails.directory_list_exist import DirectoryListExistEvasion
from .guardrails.directory_list_missing import DirectoryListMissingEvasion
from .guardrails.directory_missing import DirectoryMissingEvasion
from .guardrails.domain import DomainEvasion
from .guardrails.env_var import EnvVarEvasion
from .guardrails.expire import ExpireEvasion
from .guardrails.file_content import FileContentEvasion
from .guardrails.file_exist import FileExistEvasion
from .guardrails.file_list_exist import FileListExistEvasion
from .guardrails.file_list_missing import FileListMissingEvasion
from .guardrails.file_missing import FileMissingEvasion
from .guardrails.file_size import FileSizeEvasion
from .guardrails.hostname import HostnameEvasion
from .guardrails.installed_software import InstalledSoftwareEvasion
from .guardrails.integrity import IntegrityEvasion
from .guardrails.ip_address import IPAddressEvasion
from .guardrails.language_locale import LanguageLocaleEvasion
from .guardrails.mac_address import MACAddressEvasion
from .guardrails.macos_sip import MacSIPEvasion
from .guardrails.macos_version import MacVersionEvasion
from .guardrails.timezone import TimezoneEvasion
from .guardrails.uid import LinuxUIDEvasion
from .guardrails.username import UsernameEvasion
from .guardrails.win_ad_domain import WinADDomainEvasion
from .guardrails.win_privilege import WinPrivilegeEvasion
from .guardrails.win_prompt import WinPromptEvasion
from .multi import MultiEvasion
from .sandbox.cpu_count import CPUCountEvasion
from .sandbox.disk_size import DiskSizeEvasion
from .sandbox.edr import LinuxEDREvasion, MacEDREvasion, WinEDREvasion
from .sandbox.exec_method import ExecMethodEvasion
from .sandbox.executable_path import ExecPathEvasion
from .sandbox.linux_mouse import LinuxMouseEvasion
from .sandbox.linux_process_list import LinuxProcessListEvasion
from .sandbox.linux_sandbox_artifacts import LinuxSandboxArtifactEvasion
from .sandbox.linux_screen_resolution import LinuxScreenResolutionEvasion
from .sandbox.linux_tmp_count import LinuxTmpCountEvasion
from .sandbox.macos_disk_size import MacDiskSizeEvasion
from .sandbox.macos_mouse import MacMouseEvasion
from .sandbox.macos_process_list import MacProcessListEvasion
from .sandbox.macos_ram_count import MacRAMCountEvasion
from .sandbox.macos_sandbox_artifacts import MacSandboxArtifactEvasion
from .sandbox.macos_screen_resolution import MacScreenResolutionEvasion
from .sandbox.macos_tmp_count import MacTmpCountEvasion
from .sandbox.macos_uptime import MacUptimeEvasion
from .sandbox.macos_vm import MacVMEvasion
from .sandbox.proc_count import LinuxProcCountEvasion
from .sandbox.ram_count import LinuxRAMCountEvasion
from .sandbox.sandbox_hostname import SandboxHostnameEvasion
from .sandbox.sandbox_username import SandboxUsernameEvasion
from .sandbox.tmp_count import TmpCountEvasion
from .sandbox.uptime import LinuxUptimeEvasion
from .sandbox.utc import UTCEvasion
from .sandbox.vm_hypervisor import VMHypervisorEvasion
from .sandbox.win_mouse import WinMouseEvasion
from .sandbox.win_proc_count import WinProcCountEvasion
from .sandbox.win_process_list import WinProcessListEvasion
from .sandbox.win_ram_count import WinRAMCountEvasion
from .sandbox.win_registry_vm import WinRegistryVMEvasion
from .sandbox.win_sandbox_artifacts import WinSandboxArtifactEvasion
from .sandbox.win_screen_resolution import WinScreenResolutionEvasion
from .sandbox.win_tmp_count import WinTmpCountEvasion
from .sandbox.win_uptime import WinUptimeEvasion
from .special.cicd import CICDEvasion
from .special.jupyter import JupyterEvasion
from .special.linux_docker import LinuxDockerEvasion
from .special.linux_kubernetes import LinuxKubernetesEvasion
from .special.linux_wsl import LinuxWSLEvasion
from .special.macos_app_sandbox import MacAppSandboxEvasion
from .special.serverless import ServerlessEvasion
from .special.win_container import WinContainerEvasion
from .special.win_hyper_v import WinHyperVGuestEvasion
from .special.win_sandbox_env import WinSandboxEnvEvasion

__all__ = [
    "ArgvEvasion",
    "BreakpointHookEvasion",
    "CICDEvasion",
    "CPUCountEvasion",
    "CProfileEvasion",
    "CoverageEvasion",
    "DebuggerEvasion",
    "DirectoryExistEvasion",
    "DirectoryListExistEvasion",
    "DirectoryListMissingEvasion",
    "DirectoryMissingEvasion",
    "DiskSizeEvasion",
    "DomainEvasion",
    "EnvVarEvasion",
    "ExecMethodEvasion",
    "ExecPathEvasion",
    "ExpireEvasion",
    "FileContentEvasion",
    "FileExistEvasion",
    "FileListExistEvasion",
    "FileListMissingEvasion",
    "FileMissingEvasion",
    "FileSizeEvasion",
    "HostnameEvasion",
    "IPAddressEvasion",
    "InstalledSoftwareEvasion",
    "IntegrityEvasion",
    "JupyterEvasion",
    "LanguageLocaleEvasion",
    "LinuxDebugProcessEvasion",
    "LinuxDockerEvasion",
    "LinuxEDREvasion",
    "LinuxKubernetesEvasion",
    "LinuxMouseEvasion",
    "LinuxProcCountEvasion",
    "LinuxProcessListEvasion",
    "LinuxRAMCountEvasion",
    "LinuxSandboxArtifactEvasion",
    "LinuxScreenResolutionEvasion",
    "LinuxTmpCountEvasion",
    "LinuxUIDEvasion",
    "LinuxUptimeEvasion",
    "LinuxWSLEvasion",
    "MACAddressEvasion",
    "MacAppSandboxEvasion",
    "MacDebugProcessEvasion",
    "MacDiskSizeEvasion",
    "MacEDREvasion",
    "MacMouseEvasion",
    "MacProcessListEvasion",
    "MacRAMCountEvasion",
    "MacSIPEvasion",
    "MacSandboxArtifactEvasion",
    "MacScreenResolutionEvasion",
    "MacTmpCountEvasion",
    "MacUptimeEvasion",
    "MacVMEvasion",
    "MacVersionEvasion",
    "MultiEvasion",
    "SandboxHostnameEvasion",
    "SandboxUsernameEvasion",
    "ServerlessEvasion",
    "TimezoneEvasion",
    "TmpCountEvasion",
    "TracemallocEvasion",
    "UTCEvasion",
    "UsernameEvasion",
    "VMHypervisorEvasion",
    "WinADDomainEvasion",
    "WinContainerEvasion",
    "WinDebugProcessEvasion",
    "WinDebuggerEvasion",
    "WinEDREvasion",
    "WinHyperVGuestEvasion",
    "WinMouseEvasion",
    "WinPrivilegeEvasion",
    "WinProcCountEvasion",
    "WinProcessListEvasion",
    "WinPromptEvasion",
    "WinRAMCountEvasion",
    "WinRegistryVMEvasion",
    "WinSandboxArtifactEvasion",
    "WinSandboxEnvEvasion",
    "WinScreenResolutionEvasion",
    "WinTmpCountEvasion",
    "WinUptimeEvasion",
]
