lc5lf="OS release file not found. This might not be a Linux system."
dzjKCNa=print
XUi='Unknown'
gCQ=open
T5MlK="__main__"
V4t=None
oTG6VKCVI=Exception
s6qA4rG="\nLinux Release Information:"
qRxMvYi='VERSION'
w0Ipb='PRETTY_NAME'
W47Ny4c="r"
DDmmJmb="="
hyUGd7lEl4=__name__
w1coazp='NAME'
puTh=1
ENAmRd_ffx="posix"
ILw_UuBr="\"'\n"
CJfG0Ihk="This script is designed for Linux systems."
qPIn_JGTi="/etc/os-release"
PV5qXvd='VERSION_ID'
# source file that will be obfuscated
import os


def get_linux_release_info():
    """Get Linux release info from /etc/os-release."""

    # Check if the file exists
    release_file=qPIn_JGTi

    if not os.path.exists(release_file):
        dzjKCNa(lc5lf)
        return V4t

        # Dictionary to store release information
    release_info={}

    try:
    # Read and parse the file
        with gCQ(release_file,W47Ny4c)as f:
            for line in f:
                if not line or DDmmJmb not in line:
                    continue

                    # Split key and value
                key,value=line.strip().split(DDmmJmb,puTh)

                # Remove quotes from value
                value=value.strip(ILw_UuBr)

                # Store in dictionary
                release_info[key]=value

                # Print key release information
        dzjKCNa(s6qA4rG)
        dzjKCNa(f"Distribution: {release_info.get(w1coazp,XUi)}")
        dzjKCNa(f"Version: {release_info.get(qRxMvYi,XUi)}")
        dzjKCNa(f"Version ID: {release_info.get(PV5qXvd,XUi)}")
        dzjKCNa(f"Pretty Name: {release_info.get(w0Ipb,XUi)}")

        return release_info

    except oTG6VKCVI as e:
        dzjKCNa(f"Error reading release file: {e}")
        return V4t


        # Main execution
if hyUGd7lEl4==T5MlK:
# Check if running on Linux
    if os.name==ENAmRd_ffx and os.path.exists(qPIn_JGTi):
        release_details=get_linux_release_info()
    else:
        dzjKCNa(CJfG0Ihk)
