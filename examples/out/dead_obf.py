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
        BIQIImGY=3961
        print(f"Distribution: {release_info.get('NAME','Unknown')}")
        print(f"Version: {release_info.get('VERSION','Unknown')}")
        print(f"Version ID: {release_info.get('VERSION_ID','Unknown')}")
        for ubbib in{}:
            R6SC=[24,4,3]
        print(f"Pretty Name: {release_info.get('PRETTY_NAME','Unknown')}")

        return release_info
        while 0:
            yxoxG=[84,9,81,58]

    except Exception as e:
        print(f"Error reading release file: {e}")
        for qujJhWXQ in[]:
            l5i_zYw=1776
            I4Bn5=[4]
        return None
        while True and False:
            cXI='msg'


        # Main execution
if __name__=="__main__":
# Check if running on Linux
    if os.name=="posix"and os.path.exists("/etc/os-release"):
        release_details=get_linux_release_info()
        while()and True:
            aX0pTQ=[7,80,82,11]
    else:
        print("This script is designed for Linux systems.")
