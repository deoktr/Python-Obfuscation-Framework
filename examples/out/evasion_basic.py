import sys
if(hasattr(sys,'gettrace')and sys.gettrace()is not None):
    raise Exception('DebuggerEvasion')
from datetime import datetime
if(datetime.now()>datetime(2026,4,19,23,15,18)):
    raise Exception('ExpireEvasion')
import tracemalloc
if(tracemalloc.is_tracing()):
    raise Exception('TracemallocEvasion')
import os
if(((os.sysconf('SC_PAGE_SIZE')*os.sysconf('SC_PHYS_PAGES'))/(1024.**3))<2):
    raise Exception('LinuxRAMCountEvasion')
import multiprocessing
if(multiprocessing.cpu_count()<2):
    raise Exception('CPUCountEvasion')
import os
if(os.path.isfile('/tmp/foobar')):
    raise Exception('FileMissingEvasion')
# source file that will be obfuscated
import os


def get_linux_release_info():
    """Get Linux release info from /etc/os-release."""

    # Check if the file exists
    release_file="/etc/os-release"

    if not os.path.exists(release_file):
        print("OS release file not found. This might not be a Linux system.")
        return None

        # Dictionary to store release information
    release_info={}

    try:
    # Read and parse the file
        with open(release_file,"r")as f:
            for line in f:
                if not line or"="not in line:
                    continue

                    # Split key and value
                key,value=line.strip().split("=",1)

                # Remove quotes from value
                value=value.strip("\"'\n")

                # Store in dictionary
                release_info[key]=value

                # Print key release information
        print("\nLinux Release Information:")
        print(f"Distribution: {release_info.get('NAME','Unknown')}")
        print(f"Version: {release_info.get('VERSION','Unknown')}")
        print(f"Version ID: {release_info.get('VERSION_ID','Unknown')}")
        print(f"Pretty Name: {release_info.get('PRETTY_NAME','Unknown')}")

        return release_info

    except Exception as e:
        print(f"Error reading release file: {e}")
        return None


        # Main execution
if __name__=="__main__":
# Check if running on Linux
    if os.name=="posix"and os.path.exists("/etc/os-release"):
        release_details=get_linux_release_info()
    else:
        print("This script is designed for Linux systems.")
