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

"""Utils.

Todo:
- add process list
- add list of directory
- add reverse engineering tools
- add Ansible directory
"""

# source: https://evasions.checkpoint.com/techniques/generic-os-queries.html#check-if-username-is-specific
USERNAME = [
    "admin",
    "andy",
    "honey",
    "john",
    "john doe",
    "malnetvm",
    "maltest",
    "malware",
    "roo",
    "sandbox",
    "snort",
    "tequilaboomboom",
    "test",
    "virus",
    "virusclone",
    "wilbert",
    "remnux",
    "nepenthes",  # Nepenthes
    "currentuser",  # Norman
    "username",  # ThreatExpert
    "user",  # Sandboxie
    "vmware",  # VMware
]

# source: https://evasions.checkpoint.com/techniques/generic-os-queries.html#check-if-computer-name-is-specific
HOSTNAME = [
    "klone_x64-pc",
    "tequilaboomboom",
    "TU-4NH09SMCG1HC",  # Anubis
    "InsideTm",  # Anubis
]

# source: https://github.com/PwnDexter/SharpEDRChecker/blob/master/SharpEDRChecker/EDRData.cs
EDR_LIST = [
    "activeconsole",
    "amsi.dll",
    "anti malware",
    "anti-malware",
    "antimalware",
    "anti virus",
    "anti-virus",
    "antivirus",
    "appsense",
    "authtap",
    "avast",
    "avecto",
    "canary",
    "carbonblack",
    "carbon black",
    "cb.exe",
    "ciscoamp",
    "cisco amp",
    "countercept",
    "countertack",
    "cramtray",
    "crssvc",
    "crowdstrike",
    "csagent",
    "csfalcon",
    "csshell",
    "cybereason",
    "cyclorama",
    "cylance",
    "cyoptics",
    "cyupdate",
    "cyvera",
    "cyserver",
    "cytray",
    "darktrace",
    "defendpoint",
    "defender",
    "eectrl",
    "elastic",
    "endgame",
    "f-secure",
    "forcepoint",
    "fireeye",
    "groundling",
    "GRRservic",
    "inspector",
    "ivanti",
    "kaspersky",
    "lacuna",
    "logrhythm",
    "malware",
    "mandiant",
    "mcafee",
    "morphisec",
    "msascuil",
    "msmpeng",
    "nissrv",
    "omni",
    "omniagent",
    "osquery",
    "Palo Alto Networks",
    "pgeposervice",
    "pgsystemtray",
    "privilegeguard",
    "procwall",
    "protectorservic",
    "qradar",
    "redcloak",
    "secureworks",
    "securityhealthservice",
    "semlaunchsv",
    "sentinel",
    "sepliveupdat",
    "sisidsservice",
    "sisipsservice",
    "sisipsutil",
    "smc.exe",
    "smcgui",
    "snac64",
    "sophos",
    "splunk",
    "srtsp",
    "symantec",
    "symcorpu",
    "symefasi",
    "sysinternal",
    "sysmon",
    "tanium",
    "tda.exe",
    "tdawork",
    "tpython",
    "vectra",
    "wincollect",
    "windowssensor",
    "wireshark",
    "threat",
    "xagt.exe",
    "xagtnotif.exe",
    "hurukai",
]
