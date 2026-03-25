from base64 import b64decode
from base64 import b85decode
# source file that will be obfuscated
import os


def get_linux_release_info():
    """Get Linux release info from /etc/os-release."""

    # Check if the file exists
    release_file='\u002f\u0065\u0074\u0063\u002f\u006f\u0073\u002d\u0072\u0065\u006c\u0065\u0061\u0073\u0065'

    if not os.path.exists(release_file):
        print("OS release file not found. This might not be a Linux system.")
        return None

        # Dictionary to store release information
    release_info={}

    try:
    # Read and parse the file
        with open(release_file,'r'[::-1])as f:
            for line in f:
                if not line or'='[::-1]not in line:
                    continue

                    # Split key and value
                key,value=line.strip().split('\u003d',1)

                # Remove quotes from value
                value=value.strip('\x22\x27\x0a')

                # Store in dictionary
                release_info[key]=value

                # Print key release information
        print("".join([chr(ord(i)-3)for i in'\rOlqx{#Uhohdvh#Lqirupdwlrq=']))
        print(f"Distribution: {release_info.get("".join([chr(ord(i)-3)for i in'QDPH']),'nwonknU'[::-1])}")
        print(f"Version: {release_info.get('NOISREV'[::-1],'\x55\x6e\x6b\x6e\x6f\x77\x6e')}")
        print(f"Version ID: {release_info.get("".join([chr(ord(i)-3)for i in'YHUVLRQbLG']),"".join([chr(ord(i)-3)for i in'Xqnqrzq']))}")
        print(f"Pretty Name: {release_info.get('\x50\x52\x45\x54\x54\x59\x5f\x4e\x41\x4d\x45',b64decode('VW5rbm93bg==').decode())}")

        return release_info

    except Exception as e:
        print(f"Error reading release file: {e}")
        return None


        # Main execution
if __name__=='\x5f\x5f\x6d\x61\x69\x6e\x5f\x5f':
# Check if running on Linux
    if os.name=="".join([chr(ord(i)-3)for i in'srvl{'])and os.path.exists('\x2f\x65\x74\x63\x2f\x6f\x73\x2d\x72\x65\x6c\x65\x61\x73\x65'):
        release_details=get_linux_release_info()
    else:
        print("".join([chr(ord(i)-3)for i in'Wklv#vfulsw#lv#ghvljqhg#iru#Olqx{#v|vwhpv1']))
