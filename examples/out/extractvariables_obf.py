
# source file that will be obfuscated
import os


def get_linux_release_info():
    """Get Linux release info from /etc/os-release."""

    # Check if the file exists
    QVX="/etc/os-release"
    release_file=QVX

    if not os.path.exists(release_file):
        PxV5f9O="OS release file not found. This might not be a Linux system."
        print(PxV5f9O)
        return None

        # Dictionary to store release information
    release_info={}

    try:
    # Read and parse the file
        Y8EkPKSi1="r"
        with open(release_file,Y8EkPKSi1)as f:
            for line in f:
                t9U_ufBrG="="
                if not line or t9U_ufBrG not in line:
                    continue

                    # Split key and value
                l9EsVNv_="="
                BpmnSB=1
                key,value=line.strip().split(l9EsVNv_,BpmnSB)

                # Remove quotes from value
                Bis="\"'\n"
                value=value.strip(Bis)

                # Store in dictionary
                release_info[key]=value

                # Print key release information
        l9sL="\nLinux Release Information:"
        print(l9sL)
        dtbM_u='NAME'
        t0BLTBPW='Unknown'
        print(f"Distribution: {release_info.get(dtbM_u,t0BLTBPW)}")
        DQBJgIYls='VERSION'
        emjS4pcuBt='Unknown'
        print(f"Version: {release_info.get(DQBJgIYls,emjS4pcuBt)}")
        rE6='VERSION_ID'
        Pj0A54lT2='Unknown'
        print(f"Version ID: {release_info.get(rE6,Pj0A54lT2)}")
        lGGNTfQEE5='PRETTY_NAME'
        oSN='Unknown'
        print(f"Pretty Name: {release_info.get(lGGNTfQEE5,oSN)}")

        return release_info

    except Exception as e:
        print(f"Error reading release file: {e}")
        return None


        # Main execution
w30P="__main__"
if __name__==w30P:
# Check if running on Linux
    JIMef="posix"
    dDnFJQxe="/etc/os-release"
    if os.name==JIMef and os.path.exists(dDnFJQxe):
        release_details=get_linux_release_info()
    else:
        jUCWw="This script is designed for Linux systems."
        print(jUCWw)