# source file that will be obfuscated
import os


def get_linux_release_info():
    """Get Linux release info from /etc/os-release."""

    # Check if the file exists
    release_file="/etc/os-release"

    if not os.path.exists(release_file):
        __builtins__.__dict__['print']("OS release file not found. This might not be a Linux system.")
        return __name__.__class__.__base__.__base__

        # Dictionary to store release information
    release_info={}

    try:
    # Read and parse the file
        with __builtins__.__dict__.__getitem__('open')(release_file,"r")as f:
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
        globals()['__builtins__'].__dict__['print']("\nLinux Release Information:")
        __builtins__.__dict__['print'](f"Distribution: {release_info.get('NAME','Unknown')}")
        __builtins__.__getattribute__('print')(f"Version: {release_info.get('VERSION','Unknown')}")
        __builtins__.__dict__.__getitem__('print')(f"Version ID: {release_info.get('VERSION_ID','Unknown')}")
        globals()['__builtins__'].__dict__['print'](f"Pretty Name: {release_info.get('PRETTY_NAME','Unknown')}")

        return release_info

    except globals()['__builtins__'].__dict__['Exception']as e:
        __builtins__.__getattribute__('print')(f"Error reading release file: {e}")
        return __builtins__.__dict__.__getitem__('None')


        # Main execution
if __name__=="__main__":
# Check if running on Linux
    if os.name=="posix"and os.path.exists("/etc/os-release"):
        release_details=get_linux_release_info()
    else:
        __builtins__.__dict__.__getitem__('print')("This script is designed for Linux systems.")
