from __future__ import annotations

import pof.evasion as evasion_module

# constructor defaults for evasion classes that require arguments, unlisted are
# started without parameters
CONSTRUCTOR_DEFAULTS: dict[str, dict] = {
    "DirectoryExistEvasion": {"directory": "/tmp"},
    "DirectoryListExistEvasion": {"directory_list": ["/tmp"]},
    "DirectoryListMissingEvasion": {"directory_list": ["/tmp"]},
    "DirectoryMissingEvasion": {"directory": "/tmp"},
    "DomainEvasion": {"domain": "example.com"},
    "EnvVarEvasion": {"var_name": "HOME", "expected": "/home/user"},
    "FileContentEvasion": {"file": "/tmp/test.txt", "expected_hash": "abc123"},
    "FileExistEvasion": {"file": "/tmp/test.txt"},
    "FileListExistEvasion": {"file_list": ["/tmp/test.txt"]},
    "FileListMissingEvasion": {"file_list": ["/tmp/test.txt"]},
    "FileMissingEvasion": {"file": "/tmp/test.txt"},
    "FileSizeEvasion": {"file": "/tmp/test.txt", "size": 1024},
    "HostnameEvasion": {"hostname": "localhost"},
    "IPAddressEvasion": {"ip_or_cidr": "192.168.1.1"},
    "InstalledSoftwareEvasion": {"software": ["vim"]},
    "LinuxUIDEvasion": {"uid": 1000},
    "MacDiskSizeEvasion": {"min_disk": 50 * 1024 * 1024},
    "MacProcessListEvasion": {"process_list": ["Wireshark", "lldb"]},
    "MacRAMCountEvasion": {"min_ram": 2 * 1024 * 1024 * 1024},
    "MacSIPEvasion": {"expected_enabled": True},
    "MacSandboxArtifactEvasion": {"artifacts": ["/Library/Parallels Guest Tools"]},
    "MacScreenResolutionEvasion": {"min_width": 1024},
    "MacTmpCountEvasion": {"min_count": 3},
    "MacUptimeEvasion": {"min_uptime": 600},
    "MacVersionEvasion": {"min_version": "11.0"},
    "MACAddressEvasion": {"mac": "00:11:22:33:44:55"},
    "UsernameEvasion": {"username": "testuser"},
    "WinADDomainEvasion": {"domain": "WORKGROUP"},
}


def _build_evasion_registry() -> list[tuple[str, type, dict]]:
    """Build list of (name, class, kwargs) from evasion __all__."""
    registry = []
    for name in evasion_module.__all__:
        cls = getattr(evasion_module, name)
        kwargs = CONSTRUCTOR_DEFAULTS.get(name, {})
        registry.append((name, cls, kwargs))
    return registry


EVASION_REGISTRY = _build_evasion_registry()


def pytest_generate_tests(metafunc):
    if "evasion_entry" in metafunc.fixturenames:
        metafunc.parametrize(
            "evasion_entry",
            EVASION_REGISTRY,
            ids=[name for name, _, _ in EVASION_REGISTRY],
        )
