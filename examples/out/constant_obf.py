gav="="
BdnPpox="\nLinux Release Information:"
mV8u3bj="OS release file not found. This might not be a Linux system."
MVIBY="posix"
fv3paKw="This script is designed for Linux systems."
RudUBh=Exception
Ut_HM9U4="__main__"
E3KTjq=__name__
EW4feUeq="/etc/os-release"
Fp4a8N=print
lC3q=open
taFh="r"
N8D1ITP=1
wWqNy1=None
s0qAqHq4iY="\"'\n"
# source file that will be obfuscated
import os


def get_linux_release_info():
    """Get Linux release info from /etc/os-release."""

    # Check if the file exists
    release_file=EW4feUeq

    if not os.path.exists(release_file):
        Fp4a8N(mV8u3bj)
        return wWqNy1

        # Dictionary to store release information
    release_info={}

    try:
    # Read and parse the file
        with lC3q(release_file,taFh)as f:
            for line in f:
                if not line or gav not in line:
                    continue

                    # Split key and value
                key,value=line.strip().split(gav,N8D1ITP)

                # Remove quotes from value
                value=value.strip(s0qAqHq4iY)

                # Store in dictionary
                release_info[key]=value

                # Print key release information
        Fp4a8N(BdnPpox)
        Fp4a8N(f"Distribution: {release_info.get('NAME','Unknown')}")
        Fp4a8N(f"Version: {release_info.get('VERSION','Unknown')}")
        Fp4a8N(f"Version ID: {release_info.get('VERSION_ID','Unknown')}")
        Fp4a8N(f"Pretty Name: {release_info.get('PRETTY_NAME','Unknown')}")

        return release_info

    except RudUBh as e:
        Fp4a8N(f"Error reading release file: {e}")
        return wWqNy1


        # Main execution
if E3KTjq==Ut_HM9U4:
# Check if running on Linux
    if os.name==MVIBY and os.path.exists(EW4feUeq):
        release_details=get_linux_release_info()
    else:
        Fp4a8N(fv3paKw)
