wMEJhGXd="This script is designed for Linux systems."
o4LY="/etc/os-release"
qvh="\nLinux Release Information:"
NsKbRo=1
HNQ_Yu="posix"
lz7c="__main__"
Dbi=Exception
vk9gZ=print
gcLXDWmO=__name__
Ns5fDzVtko="="
XNv="r"
z4qr="OS release file not found. This might not be a Linux system."
FYzFFj=None
ulo13USyP=open
EcQABAH0sc="\"'\n"
# source file that will be obfuscated
import os


def get_linux_release_info():
    """Get Linux release info from /etc/os-release."""

    # Check if the file exists
    release_file=o4LY

    if not os.path.exists(release_file):
        vk9gZ(z4qr)
        return FYzFFj

        # Dictionary to store release information
    release_info={}

    try:
    # Read and parse the file
        with ulo13USyP(release_file,XNv)as f:
            for line in f:
                if not line or Ns5fDzVtko not in line:
                    continue

                    # Split key and value
                key,value=line.strip().split(Ns5fDzVtko,NsKbRo)

                # Remove quotes from value
                value=value.strip(EcQABAH0sc)

                # Store in dictionary
                release_info[key]=value

                # Print key release information
        vk9gZ(qvh)
        vk9gZ(f"Distribution: {release_info.get('NAME','Unknown')}")
        vk9gZ(f"Version: {release_info.get('VERSION','Unknown')}")
        vk9gZ(f"Version ID: {release_info.get('VERSION_ID','Unknown')}")
        vk9gZ(f"Pretty Name: {release_info.get('PRETTY_NAME','Unknown')}")

        return release_info

    except Dbi as e:
        vk9gZ(f"Error reading release file: {e}")
        return FYzFFj


        # Main execution
if gcLXDWmO==lz7c:
# Check if running on Linux
    if os.name==HNQ_Yu and os.path.exists(o4LY):
        release_details=get_linux_release_info()
    else:
        vk9gZ(wMEJhGXd)
