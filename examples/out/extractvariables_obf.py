
# source file that will be obfuscated
import os


def get_linux_release_info():
    """Get Linux release info from /etc/os-release."""

    # Check if the file exists
    BNQ6q="/etc/os-release"
    release_file=BNQ6q

    if not os.path.exists(release_file):
        PrzrNr="OS release file not found. This might not be a Linux system."
        print(PrzrNr)
        return None

        # Dictionary to store release information
    release_info={}

    try:
    # Read and parse the file
        XsuOipxOs="r"
        with open(release_file,XsuOipxOs)as f:
            for line in f:
                WO1="="
                if not line or WO1 not in line:
                    continue

                    # Split key and value
                t5Jtynqxd="="
                MDDDdTk=1
                key,value=line.strip().split(t5Jtynqxd,MDDDdTk)

                # Remove quotes from value
                i9VxX_9ruy="\"'\n"
                value=value.strip(i9VxX_9ruy)

                # Store in dictionary
                release_info[key]=value

                # Print key release information
        c1bI1C="\nLinux Release Information:"
        print(c1bI1C)
        print(f"Distribution: {release_info.get('NAME','Unknown')}")
        print(f"Version: {release_info.get('VERSION','Unknown')}")
        print(f"Version ID: {release_info.get('VERSION_ID','Unknown')}")
        print(f"Pretty Name: {release_info.get('PRETTY_NAME','Unknown')}")

        return release_info

    except Exception as e:
        print(f"Error reading release file: {e}")
        return None


        # Main execution
WAiw5_="__main__"
if __name__==WAiw5_:
# Check if running on Linux
    DF3ZfWOY="posix"
    Hn6="/etc/os-release"
    if os.name==DF3ZfWOY and os.path.exists(Hn6):
        release_details=get_linux_release_info()
    else:
        cFYfXgyL5Y="This script is designed for Linux systems."
        print(cFYfXgyL5Y)