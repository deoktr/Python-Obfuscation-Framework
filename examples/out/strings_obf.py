from base64 import b64decode
from base64 import b85decode
# source file that will be obfuscated
import os


def get_linux_release_info():
    """Get Linux release info from /etc/os-release."""

    # Check if the file exists
    release_file="".join([chr(ord(i)-3)for i in'2hwf2rv0uhohdvh'])

    if not os.path.exists(release_file):
        print('\x4f\x53\x20\x72\x65\x6c\x65\x61\x73\x65\x20\x66\x69\x6c\x65\x20\x6e\x6f\x74\x20\x66\x6f\x75\x6e\x64\x2e\x20\x54\x68\x69\x73\x20\x6d\x69\x67\x68\x74\x20\x6e\x6f\x74\x20\x62\x65\x20\x61\x20\x4c\x69\x6e\x75\x78\x20\x73\x79\x73\x74\x65\x6d\x2e')
        return None

        # Dictionary to store release information
    release_info={}

    try:
    # Read and parse the file
        with open(release_file,"".join([chr(ord(i)-3)for i in'u']))as f:
            for line in f:
                if not line or'='[::-1]not in line:
                    continue

                    # Split key and value
                key,value=line.strip().split("".join([chr(ord(i)-3)for i in'@']),1)

                # Remove quotes from value
                value=value.strip('\n\'"'[::-1])

                # Store in dictionary
                release_info[key]=value

                # Print key release information
        print("".join([chr(ord(i)-3)for i in'\rOlqx{#Uhohdvh#Lqirupdwlrq=']))
        print(f"Distribution: {release_info.get(b85decode('PC-pY').decode(),'\x55\x6e\x6b\x6e\x6f\x77\x6e')}")
        print(f"Version: {release_info.get("".join([chr(ord(i)-3)for i in'YHUVLRQ']),"".join([chr(ord(i)-3)for i in'Xqnqrzq']))}")
        print(f"Version ID: {release_info.get("".join([chr(ord(i)-3)for i in'YHUVLRQbLG']),b64decode('VW5rbm93bg==').decode())}")
        print(f"Pretty Name: {release_info.get("".join([chr(ord(i)-3)for i in'SUHWW\\bQDPH']),'nwonknU'[::-1])}")

        return release_info

    except Exception as e:
        print(f"Error reading release file: {e}")
        return None


        # Main execution
if __name__==b85decode('UteuuX>MO%').decode():
# Check if running on Linux
    if os.name==b64decode('cG9zaXg=').decode()and os.path.exists('\u002f\u0065\u0074\u0063\u002f\u006f\u0073\u002d\u0072\u0065\u006c\u0065\u0061\u0073\u0065'):
        release_details=get_linux_release_info()
    else:
        print(b64decode('VGhpcyBzY3JpcHQgaXMgZGVzaWduZWQgZm9yIExpbnV4IHN5c3RlbXMu').decode())
