# Evasion Techniques Reference

_Auto-generated documentation. Do not edit manually._

**Total techniques**: 85

## Categories

- [Debugger](#debugger) (8 techniques)
- [Guardrails](#guardrails) (29 techniques)
- [Sandbox](#sandbox) (38 techniques)
- [Special](#special) (10 techniques)

---

## Debugger

### `BreakpointHookEvasion`

- **Platform**: any
- **Description**: Detects modified breakpoint hook

**Parameters**:

_No parameters_

**Example output**:

```python
import sys 
if (sys .breakpointhook is not sys .__breakpointhook__ ):
    raise Exception ('BreakpointHookEvasion')
print ("Hello, world!")
```

### `CProfileEvasion`

- **Platform**: any
- **Description**: Detects active cProfile/profile profiling

**Parameters**:

_No parameters_

**Example output**:

```python
import sys 
if (sys .getprofile ()is not None ):
    raise Exception ('CProfileEvasion')
print ("Hello, world!")
```

### `CoverageEvasion`

- **Platform**: any
- **Description**: Detects coverage.py instrumentation

**Parameters**:

_No parameters_

**Example output**:

```python
import sys 
if ("coverage"in sys .modules ):
    raise Exception ('CoverageEvasion')
print ("Hello, world!")
```

### `DebuggerEvasion`

- **Platform**: any
- **Description**: Detects Python debugger via sys.gettrace()

**Parameters**:

_No parameters_

**Example output**:

```python
import sys 
if (hasattr (sys ,'gettrace')and sys .gettrace ()is not None ):
    raise Exception ('DebuggerEvasion')
print ("Hello, world!")
```

### `LinuxDebugProcessEvasion`

- **Platform**: linux
- **Description**: Detects debugging tools by parent process name

**Parameters**:

_No parameters_

**Example output**:

```python
import os 
if (any (x in open ("/proc/"+str (os .getppid ())+"/comm").read ()for x in ["pydevd","debugpy","pdb"])):
    raise Exception ('LinuxDebugProcessEvasion')
print ("Hello, world!")
```

### `MacDebugProcessEvasion`

- **Platform**: darwin
- **Description**: Detects macOS debugging tools by parent process name

**Parameters**:

| Parameter | Type | Default |
|---|---|---|
| `debuggers` | `list[str] | None` | `None` |

**Example output**:

```python
import subprocess ,os 
if (any (x in subprocess .check_output (['ps','-o','comm=','-p',str (os .getppid ())]).decode ()for x in ['lldb','dtrace','sample','spindump','leaks'])):
    raise Exception ('MacDebugProcessEvasion')
print ("Hello, world!")
```

### `TracemallocEvasion`

- **Platform**: any
- **Description**: Detects memory profiling via tracemalloc

**Parameters**:

_No parameters_

**Example output**:

```python
import tracemalloc 
if (tracemalloc .is_tracing ()):
    raise Exception ('TracemallocEvasion')
print ("Hello, world!")
```

### `WinDebugProcessEvasion`

- **Platform**: windows
- **Description**: Detects Windows debugging tools by process name

**Parameters**:

_No parameters_

**Example output**:

```python
import subprocess 
if (any (x in subprocess .check_output (["tasklist"]).decode ().lower ()for x in ["x64dbg","x32dbg","ollydbg","windbg","ida","immunitydebugger","cheatengine"])):
    raise Exception ('WinDebugProcessEvasion')
print ("Hello, world!")
```

---

## Guardrails

### `ArgvEvasion`

- **Platform**: any
- **Description**: Validates specific command-line arguments are passed

**Parameters**:

| Parameter | Type | Default |
|---|---|---|
| `argv` | `-` | `None` |

**Example output**:

```python
import sys 
if (len (sys .argv )<=1 or not all (a in sys .argv [1 :]for a in [])):
    raise Exception ('ArgvEvasion')
print ("Hello, world!")
```

### `DirectoryExistEvasion`

- **Platform**: any
- **Description**: Validates a specific directory exists on target

**Parameters**:

| Parameter | Type | Default |
|---|---|---|
| `directory` | `-` | `_required_` |

**Example output**:

```python
import os 
if (not os .path .isdir ('example')):
    raise Exception ('DirectoryExistEvasion')
print ("Hello, world!")
```

### `DirectoryListExistEvasion`

- **Platform**: any
- **Description**: Validates all directories in a list exist on target

**Parameters**:

| Parameter | Type | Default |
|---|---|---|
| `directory_list` | `-` | `_required_` |

**Example output**:

```python
import os 
if (not all ([os .path .isdir (p )for p in 'example'])):
    raise Exception ('DirectoryListExistEvasion')
print ("Hello, world!")
```

### `DirectoryListMissingEvasion`

- **Platform**: any
- **Description**: Validates all directories in a list are absent on target

**Parameters**:

| Parameter | Type | Default |
|---|---|---|
| `directory_list` | `-` | `_required_` |

**Example output**:

```python
import os 
if (any ([os .path .isdir (p )for p in 'example'])):
    raise Exception ('DirectoryListMissingEvasion')
print ("Hello, world!")
```

### `DirectoryMissingEvasion`

- **Platform**: any
- **Description**: Validates a specific directory is absent on target

**Parameters**:

| Parameter | Type | Default |
|---|---|---|
| `directory` | `-` | `_required_` |

**Example output**:

```python
import os 
if (os .path .isdir ('example')):
    raise Exception ('DirectoryMissingEvasion')
print ("Hello, world!")
```

### `DomainEvasion`

- **Platform**: any
- **Description**: Validates target FQDN domain

**Parameters**:

| Parameter | Type | Default |
|---|---|---|
| `domain` | `-` | `_required_` |

**Example output**:

```python
import socket 
if (socket .getfqdn ()!='example'):
    raise Exception ('DomainEvasion')
print ("Hello, world!")
```

### `EnvVarEvasion`

- **Platform**: any
- **Description**: Validates target environment variable value

**Parameters**:

| Parameter | Type | Default |
|---|---|---|
| `var_name` | `str` | `_required_` |
| `expected` | `str` | `_required_` |

**Example output**:

```python
import os 
if (os .environ .get ('example')!='example'):
    raise Exception ('EnvVarEvasion')
print ("Hello, world!")
```

### `ExpireEvasion`

- **Platform**: any
- **Description**: Time-based expiration guardrail

**Parameters**:

| Parameter | Type | Default |
|---|---|---|
| `under_datetime` | `-` | `None` |

**Example output**:

```python
from datetime import datetime 
if (datetime .now ()>datetime (2026 ,4 ,19 ,13 ,16 ,5 )):
    raise Exception ('ExpireEvasion')
print ("Hello, world!")
```

### `FileContentEvasion`

- **Platform**: any
- **Description**: Validates a file's content matches expected SHA-256 hash

**Parameters**:

| Parameter | Type | Default |
|---|---|---|
| `file` | `str` | `_required_` |
| `expected_hash` | `str` | `_required_` |

**Example output**:

```python
import hashlib 
if (hashlib .sha256 (open ('example','rb').read ()).hexdigest ()!='example'):
    raise Exception ('FileContentEvasion')
print ("Hello, world!")
```

### `FileExistEvasion`

- **Platform**: any
- **Description**: Validates a specific file exists on target

**Parameters**:

| Parameter | Type | Default |
|---|---|---|
| `file` | `-` | `_required_` |

**Example output**:

```python
import os 
if (not os .path .isfile ('example')):
    raise Exception ('FileExistEvasion')
print ("Hello, world!")
```

### `FileListExistEvasion`

- **Platform**: any
- **Description**: Validates all files in a list exist on target

**Parameters**:

| Parameter | Type | Default |
|---|---|---|
| `file_list` | `-` | `_required_` |

**Example output**:

```python
import os 
if (not all ([os .path .isfile (p )for p in 'example'])):
    raise Exception ('FileListExistEvasion')
print ("Hello, world!")
```

### `FileListMissingEvasion`

- **Platform**: any
- **Description**: Validates all files in a list are absent on target

**Parameters**:

| Parameter | Type | Default |
|---|---|---|
| `file_list` | `-` | `_required_` |

**Example output**:

```python
import os 
if (any ([os .path .isfile (p )for p in 'example'])):
    raise Exception ('FileListMissingEvasion')
print ("Hello, world!")
```

### `FileMissingEvasion`

- **Platform**: any
- **Description**: Validates a specific file is absent on target

**Parameters**:

| Parameter | Type | Default |
|---|---|---|
| `file` | `-` | `_required_` |

**Example output**:

```python
import os 
if (os .path .isfile ('example')):
    raise Exception ('FileMissingEvasion')
print ("Hello, world!")
```

### `FileSizeEvasion`

- **Platform**: any
- **Description**: Validates a specific file matches expected size

**Parameters**:

| Parameter | Type | Default |
|---|---|---|
| `file` | `str` | `_required_` |
| `size` | `int` | `_required_` |

**Example output**:

```python
import os 
if (os .path .getsize ('example')!=2 ):
    raise Exception ('FileSizeEvasion')
print ("Hello, world!")
```

### `HostnameEvasion`

- **Platform**: any
- **Description**: Validates target hostname

**Parameters**:

| Parameter | Type | Default |
|---|---|---|
| `hostname` | `-` | `_required_` |

**Example output**:

```python
import socket 
if (socket .gethostname ()!='example'):
    raise Exception ('HostnameEvasion')
print ("Hello, world!")
```

### `IPAddressEvasion`

- **Platform**: any
- **Description**: Validates target IP address or CIDR range

**Parameters**:

| Parameter | Type | Default |
|---|---|---|
| `ip_or_cidr` | `str` | `_required_` |

**Example output**:

```python
import socket ;import ipaddress 
if (not ipaddress .ip_address (socket .gethostbyname (socket .gethostname ()))in ipaddress .ip_network ('example',strict =False )):
    raise Exception ('IPAddressEvasion')
print ("Hello, world!")
```

### `InstalledSoftwareEvasion`

- **Platform**: any
- **Description**: Validates required software is installed on target

**Parameters**:

| Parameter | Type | Default |
|---|---|---|
| `software` | `list[str]` | `_required_` |

**Example output**:

```python
import shutil 
if (not all (shutil .which (s )is not None for s in 'example')):
    raise Exception ('InstalledSoftwareEvasion')
print ("Hello, world!")
```

### `IntegrityEvasion`

- **Platform**: any
- **Description**: Detects source code tampering via hash verification

**Parameters**:

_No parameters_

**Example output**:

```python
import hashlib ,inspect 
def integrity (ihash ):
    stack =""
    for obj in [integrity ]:
        stack +=inspect .getsource (obj )
    m =hashlib .sha3_512 ()
    m .update (stack .encode ())
    m .digest ()
    h =m .hexdigest ()
    return h !=ihash 
if (integrity ("a")):
    raise Exception ('IntegrityEvasion')
print ("Hello, world!")
```

### `LanguageLocaleEvasion`

- **Platform**: any
- **Description**: Validates target system language locale

**Parameters**:

| Parameter | Type | Default |
|---|---|---|
| `language` | `str` | `'en'` |

**Example output**:

```python
import locale 
if (locale .getdefaultlocale ()[0 ]is None or not locale .getdefaultlocale ()[0 ].startswith ('en')):
    raise Exception ('LanguageLocaleEvasion')
print ("Hello, world!")
```

### `LinuxUIDEvasion`

- **Platform**: linux
- **Description**: Validates target Linux UID

**Parameters**:

| Parameter | Type | Default |
|---|---|---|
| `uid` | `-` | `_required_` |

**Example output**:

```python
import os 
if (os .getuid ()!=example ):
    raise Exception ('LinuxUIDEvasion')
print ("Hello, world!")
```

### `MACAddressEvasion`

- **Platform**: any
- **Description**: Validates target MAC address

**Parameters**:

| Parameter | Type | Default |
|---|---|---|
| `mac` | `str` | `_required_` |

**Example output**:

```python
# Example not available: invalid literal for int() with base 16: 'example'
```

### `MacSIPEvasion`

- **Platform**: darwin
- **Description**: Checks macOS System Integrity Protection (SIP) status

**Parameters**:

| Parameter | Type | Default |
|---|---|---|
| `expected_enabled` | `bool` | `True` |

**Example output**:

```python
import subprocess 
if ((b"enabled"in subprocess .check_output (['csrutil','status']))!=True ):
    raise Exception ('MacSIPEvasion')
print ("Hello, world!")
```

### `MacVersionEvasion`

- **Platform**: darwin
- **Description**: Checks macOS version against a minimum version

**Parameters**:

| Parameter | Type | Default |
|---|---|---|
| `min_version` | `str` | `'11.0'` |

**Example output**:

```python
import platform 
if (tuple (int (x )for x in platform .mac_ver ()[0 ].split ('.'))<tuple (int (x )for x in '11.0'.split ('.'))):
    raise Exception ('MacVersionEvasion')
print ("Hello, world!")
```

### `TimezoneEvasion`

- **Platform**: any
- **Description**: Validates target system timezone

**Parameters**:

| Parameter | Type | Default |
|---|---|---|
| `timezone` | `str` | `'UTC'` |

**Example output**:

```python
import time 
if (time .tzname [0 ]!='UTC'):
    raise Exception ('TimezoneEvasion')
print ("Hello, world!")
```

### `UsernameEvasion`

- **Platform**: any
- **Description**: Validates target username

**Parameters**:

| Parameter | Type | Default |
|---|---|---|
| `username` | `-` | `_required_` |

**Example output**:

```python
import getpass 
if (getpass .getuser ()!='example'):
    raise Exception ('UsernameEvasion')
print ("Hello, world!")
```

### `WinADDomainEvasion`

- **Platform**: windows
- **Description**: Validates target Active Directory domain

**Parameters**:

| Parameter | Type | Default |
|---|---|---|
| `domain` | `str` | `_required_` |

**Example output**:

```python
import os 
if (os .environ .get ('USERDNSDOMAIN','').lower ()!='example'):
    raise Exception ('WinADDomainEvasion')
print ("Hello, world!")
```

### `WinDebuggerEvasion`

- **Platform**: windows
- **Description**: Detects attached debugger on Windows via IsDebuggerPresent

**Parameters**:

_No parameters_

**Example output**:

```python
import ctypes 
if (ctypes .windll .kernel32 .IsDebuggerPresent ()):
    raise Exception ('WinDebuggerEvasion')
print ("Hello, world!")
```

### `WinPrivilegeEvasion`

- **Platform**: windows
- **Description**: Checks if running with administrator privileges on Windows

**Parameters**:

_No parameters_

**Example output**:

```python
import ctypes 
if (not ctypes .windll .shell32 .IsUserAnAdmin ()):
    raise Exception ('WinPrivilegeEvasion')
print ("Hello, world!")
```

### `WinPromptEvasion`

- **Platform**: windows
- **Description**: Prompts user for confirmation before execution (Windows)

**Parameters**:

| Parameter | Type | Default |
|---|---|---|
| `title` | `-` | `None` |
| `message` | `-` | `None` |

**Example output**:

```python
import ctypes 
if (not ctypes .windll .user32 .MessageBoxW (None ,'Your system encountered an error, please click OK to proceed','System Error 0x18463832')):
    raise Exception ('WinPromptEvasion')
print ("Hello, world!")
```

---

## Sandbox

### `CPUCountEvasion`

- **Platform**: any
- **Description**: Detects low CPU count indicating a sandbox VM

**Parameters**:

| Parameter | Type | Default |
|---|---|---|
| `min_cpu_count` | `int` | `2` |

**Example output**:

```python
import multiprocessing 
if (multiprocessing .cpu_count ()<2 ):
    raise Exception ('CPUCountEvasion')
print ("Hello, world!")
```

### `DiskSizeEvasion`

- **Platform**: any
- **Description**: Detects small disk size indicating a sandbox VM

**Parameters**:

| Parameter | Type | Default |
|---|---|---|
| `min_gb` | `int` | `60` |

**Example output**:

```python
import shutil 
if (shutil .disk_usage ('/').total /(1024 **3 )<60 ):
    raise Exception ('DiskSizeEvasion')
print ("Hello, world!")
```

### `ExecMethodEvasion`

- **Platform**: any
- **Description**: Detects execution method (file vs memory/stdin)

**Parameters**:

| Parameter | Type | Default |
|---|---|---|
| `method` | `-` | `'file'` |

**Example output**:

```python
import time 
if (__file__ =='<stdin>' ):
    raise Exception ('ExecMethodEvasion')
print ("Hello, world!")
```

### `ExecPathEvasion`

- **Platform**: any
- **Description**: Detects sandbox-related keywords in executable path

**Parameters**:

| Parameter | Type | Default |
|---|---|---|
| `contain_list` | `-` | `('virus', 'VIRUS', 'sample', 'SAMPLE', 'sandbox', 'SANDBOX', 'malware', 'Malware', 'InsideTm', 'insidetm')` |

**Example output**:

```python
import pathlib 
if (any ([s in str (pathlib .Path (__file__ ).absolute ())for s in ('virus','VIRUS','sample','SAMPLE','sandbox','SANDBOX','malware','Malware','InsideTm','insidetm')])):
    raise Exception ('ExecPathEvasion')
print ("Hello, world!")
```

### `LinuxEDREvasion`

- **Platform**: linux
- **Description**: Detects EDR/security products via Linux process list

**Parameters**:

| Parameter | Type | Default |
|---|---|---|
| `edr_list` | `list[str] | None` | `None` |

**Example output**:

```python
import subprocess 
if (any (e in subprocess .check_output (['ps','-eo','comm']).decode ().lower ()for e in ['activeconsole','amsi.dll','anti malware','anti-malware','antimalware','anti virus','anti-virus','antivirus','appsense','authtap','avast','avecto','canary','carbonblack','carbon black','cb.exe','ciscoamp','cisco amp','countercept','countertack','cramtray','crssvc','crowdstrike','csagent','csfalcon','csshell','cybereason','cyclorama','cylance','cyoptics','cyupdate','cyvera','cyserver','cytray','darktrace','defendpoint','defender','eectrl','elastic','endgame','f-secure','forcepoint','fireeye','groundling','GRRservic','inspector','ivanti','kaspersky','lacuna','logrhythm','malware','mandiant','mcafee','morphisec','msascuil','msmpeng','nissrv','omni','omniagent','osquery','Palo Alto Networks','pgeposervice','pgsystemtray','privilegeguard','procwall','protectorservic','qradar','redcloak','secureworks','securityhealthservice','semlaunchsv','sentinel','sepliveupdat','sisidsservice','sisipsservice','sisipsutil','smc.exe','smcgui','snac64','sophos','splunk','srtsp','symantec','symcorpu','symefasi','sysinternal','sysmon','tanium','tda.exe','tdawork','tpython','vectra','wincollect','windowssensor','wireshark','threat','xagt.exe','xagtnotif.exe','hurukai'])):
    raise Exception ('LinuxEDREvasion')
print ("Hello, world!")
```

### `LinuxMouseEvasion`

- **Platform**: linux
- **Description**: Detects absence of mouse input devices indicating a headless sandbox

**Parameters**:

_No parameters_

**Example output**:

```python
import os 
if (not any ('mouse'in f .lower ()for f in os .listdir ('/dev/input/by-id/'))if os .path .isdir ('/dev/input/by-id/')else True ):
    raise Exception ('LinuxMouseEvasion')
print ("Hello, world!")
```

### `LinuxProcCountEvasion`

- **Platform**: linux
- **Description**: Detects low process count indicating a sandbox VM

**Parameters**:

| Parameter | Type | Default |
|---|---|---|
| `proc_count` | `-` | `100` |

**Example output**:

```python
import os 
if (len (list (filter (lambda d :d .isdigit (),os .listdir ('/proc'))))<100 ):
    raise Exception ('LinuxProcCountEvasion')
print ("Hello, world!")
```

### `LinuxProcessListEvasion`

- **Platform**: linux
- **Description**: Detects known analysis tool processes running on the system

**Parameters**:

_No parameters_

**Example output**:

```python
import subprocess 
if (any (x in subprocess .check_output (['ps','-eo','comm']).decode ()for x in ['wireshark','tcpdump','strace','ltrace','gdb'])):
    raise Exception ('LinuxProcessListEvasion')
print ("Hello, world!")
```

### `LinuxRAMCountEvasion`

- **Platform**: linux
- **Description**: Detects low RAM indicating a sandbox VM

**Parameters**:

| Parameter | Type | Default |
|---|---|---|
| `min_ram` | `int` | `2` |

**Example output**:

```python
import os 
if (((os .sysconf ('SC_PAGE_SIZE')*os .sysconf ('SC_PHYS_PAGES'))/(1024. **3 ))<2 ):
    raise Exception ('LinuxRAMCountEvasion')
print ("Hello, world!")
```

### `LinuxSandboxArtifactEvasion`

- **Platform**: linux
- **Description**: Detects known sandbox/VM artifact files on the filesystem

**Parameters**:

| Parameter | Type | Default |
|---|---|---|
| `artifacts` | `list[str] | None` | `None` |

**Example output**:

```python
import os 
if (any (os .path .exists (a )for a in ['/usr/bin/VBoxService','/usr/bin/vmtoolsd','/usr/bin/qemu-ga','/proc/scsi/scsi'])):
    raise Exception ('LinuxSandboxArtifactEvasion')
print ("Hello, world!")
```

### `LinuxScreenResolutionEvasion`

- **Platform**: linux
- **Description**: Detects low screen resolution in X11 indicating a headless sandbox

**Parameters**:

| Parameter | Type | Default |
|---|---|---|
| `min_width` | `int` | `1024` |
| `min_height` | `int` | `768` |

**Example output**:

```python
import subprocess 
if (int (subprocess .check_output (['xrandr']).decode ().split ('current')[1 ].split (',')[0 ].strip ().split (' x ')[0 ])<1024 ):
    raise Exception ('LinuxScreenResolutionEvasion')
print ("Hello, world!")
```

### `LinuxTmpCountEvasion`

- **Platform**: linux
- **Description**: Detects low temp file count on Linux

**Parameters**:

| Parameter | Type | Default |
|---|---|---|
| `tmp_count` | `-` | `5` |

**Example output**:

```python
import os ,sys 
if (len (os .listdir ('/tmp'))<5 ):
    raise Exception ('LinuxTmpCountEvasion')
print ("Hello, world!")
```

### `LinuxUptimeEvasion`

- **Platform**: linux
- **Description**: Detects low system uptime indicating a fresh VM

**Parameters**:

| Parameter | Type | Default |
|---|---|---|
| `uptime` | `-` | `720` |

**Example output**:

```python
from pathlib import Path 
if (float (Path ('/proc/uptime').read_text ().split ()[0 ])<720 ):
    raise Exception ('LinuxUptimeEvasion')
print ("Hello, world!")
```

### `MacDiskSizeEvasion`

- **Platform**: darwin
- **Description**: Detects small disk size on macOS indicating a sandbox VM

**Parameters**:

| Parameter | Type | Default |
|---|---|---|
| `min_disk` | `int` | `52428800` |

**Example output**:

```python
import subprocess 
if (int (subprocess .check_output (['df','-k','/']).decode ().split ('\n')[1 ].split ()[1 ])<52428800 ):
    raise Exception ('MacDiskSizeEvasion')
print ("Hello, world!")
```

### `MacEDREvasion`

- **Platform**: darwin
- **Description**: Detects EDR/security products via macOS process list

**Parameters**:

| Parameter | Type | Default |
|---|---|---|
| `edr_list` | `list[str] | None` | `None` |

**Example output**:

```python
import subprocess 
if (any (e in subprocess .check_output (['ps','-eo','comm']).decode ().lower ()for e in ['cbosxsensorservice','cbdefense','sentinelagent','falcond','crowdstrike','malwarebytes','littlesnitch','lulu'])):
    raise Exception ('MacEDREvasion')
print ("Hello, world!")
```

### `MacMouseEvasion`

- **Platform**: darwin
- **Description**: Detects absence of mouse/trackpad on macOS via IORegistry

**Parameters**:

_No parameters_

**Example output**:

```python
import subprocess 
if (b"AppleHIDMouseDevice"not in subprocess .check_output (['ioreg','-c','AppleHIDMouseDevice','-r'])):
    raise Exception ('MacMouseEvasion')
print ("Hello, world!")
```

### `MacProcessListEvasion`

- **Platform**: darwin
- **Description**: Detects known analysis tool processes on macOS

**Parameters**:

| Parameter | Type | Default |
|---|---|---|
| `process_list` | `list[str] | None` | `None` |

**Example output**:

```python
import subprocess 
if (any (x in subprocess .check_output (['ps','-eo','comm']).decode ()for x in ['Wireshark','tcpdump','dtrace','lldb','fsmon','filemon','procmon','Instruments'])):
    raise Exception ('MacProcessListEvasion')
print ("Hello, world!")
```

### `MacRAMCountEvasion`

- **Platform**: darwin
- **Description**: Detects low RAM on macOS indicating a sandbox VM

**Parameters**:

| Parameter | Type | Default |
|---|---|---|
| `min_ram` | `int` | `2147483648` |

**Example output**:

```python
import subprocess 
if (int (subprocess .check_output (['sysctl','-n','hw.memsize']).strip ())<2147483648 ):
    raise Exception ('MacRAMCountEvasion')
print ("Hello, world!")
```

### `MacSandboxArtifactEvasion`

- **Platform**: darwin
- **Description**: Detects known sandbox/VM artifact files on macOS

**Parameters**:

| Parameter | Type | Default |
|---|---|---|
| `artifacts` | `list[str] | None` | `None` |

**Example output**:

```python
import os 
if (any (os .path .exists (a )for a in ['/Library/Parallels Guest Tools','/Library/Application Support/VMware Tools','/usr/local/bin/VBoxControl','/Library/LaunchDaemons/com.parallels.vm.prl_nettool.plist'])):
    raise Exception ('MacSandboxArtifactEvasion')
print ("Hello, world!")
```

### `MacScreenResolutionEvasion`

- **Platform**: darwin
- **Description**: Detects low screen resolution on macOS indicating a headless sandbox

**Parameters**:

| Parameter | Type | Default |
|---|---|---|
| `min_width` | `int` | `1024` |

**Example output**:

```python
import subprocess 
if (int (subprocess .check_output (['osascript','-e','tell application "Finder" to get bounds of window of desktop']).decode ().split (', ')[2 ])<1024 ):
    raise Exception ('MacScreenResolutionEvasion')
print ("Hello, world!")
```

### `MacTmpCountEvasion`

- **Platform**: darwin
- **Description**: Detects low temp file count on macOS

**Parameters**:

| Parameter | Type | Default |
|---|---|---|
| `min_count` | `int` | `3` |

**Example output**:

```python
import os 
if (len (os .listdir ('/private/tmp'))<3 ):
    raise Exception ('MacTmpCountEvasion')
print ("Hello, world!")
```

### `MacUptimeEvasion`

- **Platform**: darwin
- **Description**: Detects low uptime on macOS indicating a recently booted sandbox

**Parameters**:

| Parameter | Type | Default |
|---|---|---|
| `min_uptime` | `int` | `600` |

**Example output**:

```python
import subprocess ,time 
if (time .time ()-int (subprocess .check_output (['sysctl','-n','kern.boottime']).decode ().split ('sec = ')[1 ].split (',')[0 ])<600 ):
    raise Exception ('MacUptimeEvasion')
print ("Hello, world!")
```

### `MacVMEvasion`

- **Platform**: darwin
- **Description**: Detects VM/hypervisor on macOS via sysctl CPU VMM flag

**Parameters**:

_No parameters_

**Example output**:

```python
import subprocess 
if (b"VMM"in subprocess .check_output (['sysctl','-n','machdep.cpu.features'])):
    raise Exception ('MacVMEvasion')
print ("Hello, world!")
```

### `SandboxHostnameEvasion`

- **Platform**: any
- **Description**: Detects known sandbox hostnames via socket.gethostname()

**Parameters**:

| Parameter | Type | Default |
|---|---|---|
| `hostnames` | `list[str] | None` | `None` |

**Example output**:

```python
import socket 
if (socket .gethostname ()in ['klone_x64-pc','tequilaboomboom','TU-4NH09SMCG1HC','InsideTm']):
    raise Exception ('SandboxHostnameEvasion')
print ("Hello, world!")
```

### `SandboxUsernameEvasion`

- **Platform**: any
- **Description**: Detects known sandbox usernames via getpass.getuser()

**Parameters**:

| Parameter | Type | Default |
|---|---|---|
| `usernames` | `list[str] | None` | `None` |

**Example output**:

```python
import getpass 
if (getpass .getuser ().lower ()in ['admin','andy','honey','john','john doe','malnetvm','maltest','malware','roo','sandbox','snort','tequilaboomboom','test','virus','virusclone','wilbert','remnux','nepenthes','currentuser','username','user','vmware']):
    raise Exception ('SandboxUsernameEvasion')
print ("Hello, world!")
```

### `TmpCountEvasion`

- **Platform**: any
- **Description**: Detects low temp file count indicating a sandbox

**Parameters**:

| Parameter | Type | Default |
|---|---|---|
| `tmp_count` | `-` | `5` |

**Example output**:

```python
import os ,sys 
if (len (os .listdir ('/tmp'if sys .platform !='windows'else 'C:\\windows\\temp'))<5 ):
    raise Exception ('TmpCountEvasion')
print ("Hello, world!")
```

### `UTCEvasion`

- **Platform**: any
- **Description**: Detects UTC timezone commonly used in sandboxes

**Parameters**:

_No parameters_

**Example output**:

```python
import time 
if ("UTC"in time .tzname ):
    raise Exception ('UTCEvasion')
print ("Hello, world!")
```

### `VMHypervisorEvasion`

- **Platform**: any
- **Description**: Detects VM via MAC OUI prefix check using uuid.getnode()

**Parameters**:

_No parameters_

**Example output**:

```python
import uuid 
if ((uuid .getnode ()>>24 )in [0x000C29 ,0x001C14 ,0x005056 ,0x0003FF ,0x00155D ,0x080027 ,0x0A0027 ,0x525400 ]):
    raise Exception ('VMHypervisorEvasion')
print ("Hello, world!")
```

### `WinEDREvasion`

- **Platform**: windows
- **Description**: Detects EDR/security products via Windows task list

**Parameters**:

| Parameter | Type | Default |
|---|---|---|
| `edr_list` | `list[str] | None` | `None` |

**Example output**:

```python
import subprocess 
if (any (e in subprocess .check_output (['tasklist']).decode ().lower ()for e in ['activeconsole','amsi.dll','anti malware','anti-malware','antimalware','anti virus','anti-virus','antivirus','appsense','authtap','avast','avecto','canary','carbonblack','carbon black','cb.exe','ciscoamp','cisco amp','countercept','countertack','cramtray','crssvc','crowdstrike','csagent','csfalcon','csshell','cybereason','cyclorama','cylance','cyoptics','cyupdate','cyvera','cyserver','cytray','darktrace','defendpoint','defender','eectrl','elastic','endgame','f-secure','forcepoint','fireeye','groundling','GRRservic','inspector','ivanti','kaspersky','lacuna','logrhythm','malware','mandiant','mcafee','morphisec','msascuil','msmpeng','nissrv','omni','omniagent','osquery','Palo Alto Networks','pgeposervice','pgsystemtray','privilegeguard','procwall','protectorservic','qradar','redcloak','secureworks','securityhealthservice','semlaunchsv','sentinel','sepliveupdat','sisidsservice','sisipsservice','sisipsutil','smc.exe','smcgui','snac64','sophos','splunk','srtsp','symantec','symcorpu','symefasi','sysinternal','sysmon','tanium','tda.exe','tdawork','tpython','vectra','wincollect','windowssensor','wireshark','threat','xagt.exe','xagtnotif.exe','hurukai'])):
    raise Exception ('WinEDREvasion')
print ("Hello, world!")
```

### `WinMouseEvasion`

- **Platform**: windows
- **Description**: Detects absence of mouse device on Windows indicating a headless sandbox

**Parameters**:

_No parameters_

**Example output**:

```python
import ctypes 
if (ctypes .windll .user32 .GetSystemMetrics (19 )==0 ):
    raise Exception ('WinMouseEvasion')
print ("Hello, world!")
```

### `WinProcCountEvasion`

- **Platform**: windows
- **Description**: Detects low process count on Windows indicating a sandbox VM

**Parameters**:

| Parameter | Type | Default |
|---|---|---|
| `proc_count` | `int` | `50` |

**Example output**:

```python
import subprocess 
if (len (subprocess .check_output (['tasklist']).decode ().strip ().split ('\n'))<50 ):
    raise Exception ('WinProcCountEvasion')
print ("Hello, world!")
```

### `WinProcessListEvasion`

- **Platform**: windows
- **Description**: Detects known analysis tool processes on Windows

**Parameters**:

_No parameters_

**Example output**:

```python
import subprocess 
if (any (x in subprocess .check_output (['tasklist']).decode ().lower ()for x in ['wireshark','procmon','processhacker','fiddler','x64dbg','autoruns','tcpview'])):
    raise Exception ('WinProcessListEvasion')
print ("Hello, world!")
```

### `WinRAMCountEvasion`

- **Platform**: windows
- **Description**: Detects low RAM on Windows indicating a sandbox VM

**Parameters**:

| Parameter | Type | Default |
|---|---|---|
| `min_ram` | `int` | `2` |

**Example output**:

```python
import os 
if (int (os .popen ('wmic ComputerSystem get TotalPhysicalMemory').read ().split ()[-1 ])//(1024 **3 )<2 ):
    raise Exception ('WinRAMCountEvasion')
print ("Hello, world!")
```

### `WinRegistryVMEvasion`

- **Platform**: windows
- **Description**: Detects VM indicators in Windows registry BIOS information

**Parameters**:

_No parameters_

**Example output**:

```python
import os 
if (any (k in os .popen ('reg query HKLM\\HARDWARE\\DESCRIPTION\\System\\BIOS /v SystemManufacturer').read ()for k in ['VirtualBox','VMware','QEMU','Xen','innotek'])):
    raise Exception ('WinRegistryVMEvasion')
print ("Hello, world!")
```

### `WinSandboxArtifactEvasion`

- **Platform**: windows
- **Description**: Detects known sandbox/VM artifact files on Windows

**Parameters**:

| Parameter | Type | Default |
|---|---|---|
| `artifacts` | `list[str] | None` | `None` |

**Example output**:

```python
import os 
if (any (os .path .exists (a )for a in ['C:\\Windows\\System32\\drivers\\VBoxMouse.sys','C:\\Windows\\System32\\drivers\\vmhgfs.sys','C:\\Windows\\System32\\drivers\\vm3dmp.sys','C:\\Program Files\\VMware\\VMware Tools','c:\\windows\\system32\\drivers\\vmsrvc.sys','c:\\windows\\system32\\drivers\\vpc-s3.sys','c:\\windows\\system32\\drivers\\prleth.sys'])):
    raise Exception ('WinSandboxArtifactEvasion')
print ("Hello, world!")
```

### `WinScreenResolutionEvasion`

- **Platform**: windows
- **Description**: Detects low screen resolution on Windows indicating a headless sandbox

**Parameters**:

| Parameter | Type | Default |
|---|---|---|
| `min_width` | `int` | `1024` |
| `min_height` | `int` | `768` |

**Example output**:

```python
import ctypes 
if (ctypes .windll .user32 .GetSystemMetrics (0 )<1024 ):
    raise Exception ('WinScreenResolutionEvasion')
print ("Hello, world!")
```

### `WinTmpCountEvasion`

- **Platform**: windows
- **Description**: Detects low temp file count on Windows

**Parameters**:

| Parameter | Type | Default |
|---|---|---|
| `tmp_count` | `-` | `5` |

**Example output**:

```python
import os ,sys 
if (len (os .listdir ('C:\\windows\\temp'))<5 ):
    raise Exception ('WinTmpCountEvasion')
print ("Hello, world!")
```

### `WinUptimeEvasion`

- **Platform**: windows
- **Description**: Detects low system uptime on Windows indicating a fresh sandbox VM

**Parameters**:

| Parameter | Type | Default |
|---|---|---|
| `uptime` | `int` | `720000` |

**Example output**:

```python
import ctypes 
if (ctypes .windll .kernel32 .GetTickCount64 ()<720000 ):
    raise Exception ('WinUptimeEvasion')
print ("Hello, world!")
```

---

## Special

### `CICDEvasion`

- **Platform**: any
- **Description**: Detects CI/CD pipeline execution

**Parameters**:

_No parameters_

**Example output**:

```python
import os 
if (any (os .environ .get (v )is not None for v in ["GITHUB_ACTIONS","GITLAB_CI","JENKINS_URL","CIRCLECI","TRAVIS","BUILDKITE","TF_BUILD","TEAMCITY_VERSION"])):
    raise Exception ('CICDEvasion')
print ("Hello, world!")
```

### `JupyterEvasion`

- **Platform**: any
- **Description**: Detects Jupyter/IPython notebook execution

**Parameters**:

_No parameters_

**Example output**:

```python
import sys 
if ("IPython"in sys .modules or "ipykernel"in sys .modules ):
    raise Exception ('JupyterEvasion')
print ("Hello, world!")
```

### `LinuxDockerEvasion`

- **Platform**: linux
- **Description**: Detects Docker container execution

**Parameters**:

_No parameters_

**Example output**:

```python
import os 
if (os .path .exists ("/.dockerenv")or (os .path .exists ("/proc/1/cgroup")and "docker"in open ("/proc/1/cgroup").read ())):
    raise Exception ('LinuxDockerEvasion')
print ("Hello, world!")
```

### `LinuxKubernetesEvasion`

- **Platform**: linux
- **Description**: Detects Kubernetes pod execution

**Parameters**:

_No parameters_

**Example output**:

```python
import os 
if (os .path .isdir ("/var/run/secrets/kubernetes.io")or os .environ .get ("KUBERNETES_SERVICE_HOST")is not None ):
    raise Exception ('LinuxKubernetesEvasion')
print ("Hello, world!")
```

### `LinuxWSLEvasion`

- **Platform**: linux
- **Description**: Detects Windows Subsystem for Linux execution

**Parameters**:

_No parameters_

**Example output**:

```python
import os 
if (os .path .exists ("/proc/version")and "microsoft"in open ("/proc/version").read ().lower ()):
    raise Exception ('LinuxWSLEvasion')
print ("Hello, world!")
```

### `MacAppSandboxEvasion`

- **Platform**: darwin
- **Description**: Detects macOS App Sandbox environment

**Parameters**:

_No parameters_

**Example output**:

```python
import os 
if (os .environ .get ('APP_SANDBOX_CONTAINER_ID')is not None ):
    raise Exception ('MacAppSandboxEvasion')
print ("Hello, world!")
```

### `ServerlessEvasion`

- **Platform**: any
- **Description**: Detects serverless/cloud function runtime

**Parameters**:

_No parameters_

**Example output**:

```python
import os 
if (any (os .environ .get (v )is not None for v in ["AWS_LAMBDA_FUNCTION_NAME","FUNCTIONS_WORKER_RUNTIME","K_SERVICE","GOOGLE_CLOUD_PROJECT"])):
    raise Exception ('ServerlessEvasion')
print ("Hello, world!")
```

### `WinContainerEvasion`

- **Platform**: windows
- **Description**: Detects Windows container execution

**Parameters**:

_No parameters_

**Example output**:

```python
import os 
if (os .environ .get ("CONTAINER","")!=""or os .path .exists ("C:\\ServiceProfiles")):
    raise Exception ('WinContainerEvasion')
print ("Hello, world!")
```

### `WinHyperVGuestEvasion`

- **Platform**: windows
- **Description**: Detects Hyper-V guest VM execution

**Parameters**:

_No parameters_

**Example output**:

```python
import os 
if (os .path .exists ("C:\\Windows\\System32\\drivers\\vmbus.sys")):
    raise Exception ('WinHyperVGuestEvasion')
print ("Hello, world!")
```

### `WinSandboxEnvEvasion`

- **Platform**: windows
- **Description**: Detects Windows Sandbox (Win10/11 built-in feature)

**Parameters**:

_No parameters_

**Example output**:

```python
import os 
if (os .environ .get ("USERNAME","")=="WDAGUtilityAccount"):
    raise Exception ('WinSandboxEnvEvasion')
print ("Hello, world!")
```
