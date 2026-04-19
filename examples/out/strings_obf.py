from base64 import b64decode
from base64 import b85decode
# source file that will be obfuscated
import os


def get_linux_release_info():
    """Get Linux release info from /etc/os-release."""

    # Check if the file exists
    release_file="".join([chr(ord(i)-3)for i in'2hwf2rv0uhohdvh'])

    if not os.path.exists(release_file):
        print("".join([chr(ord(i)-3)for i in'RV#uhohdvh#iloh#qrw#irxqg1#Wklv#pljkw#qrw#eh#d#Olqx{#v|vwhp1']))
        return None

        # Dictionary to store release information
    release_info={}

    try:
    # Read and parse the file
        with open(release_file,b85decode('as').decode())as f:
            for line in f:
                if not line or"".join([chr(ord(i)-3)for i in'@'])not in line:
                    continue

                    # Split key and value
                key,value=line.strip().split(b85decode('Jp').decode(),1)

                # Remove quotes from value
                value=value.strip("".join([chr(ord(i)-3)for i in'%*\r']))

                # Store in dictionary
                release_info[key]=value

                # Print key release information
        print(':noitamrofnI esaeleR xuniL\n'[::-1])
        print(f"Distribution: {release_info.get("".join([chr(ord(i)-3)for i in'QDPH']),"".join([chr(ord(i)-3)for i in'Xqnqrzq']))}")
        print(f"Version: {release_info.get('VERSION','Unknown')}")
        print(f"Version ID: {release_info.get("".join([chr(ord(i)-3)for i in'YHUVLRQbLG']),'nwonknU'[::-1])}")
        print(f"Pretty Name: {release_info.get('\x50\x52\x45\x54\x54\x59\x5f\x4e\x41\x4d\x45','\u0055\u006e\u006b\u006e\u006f\u0077\u006e')}")

        return release_info

    except Exception as e:
        print(f"Error reading release file: {e}")
        return None


        # Main execution
if __name__=="".join([chr(ord(i)-3)for i in'bbpdlqbb']):
# Check if running on Linux
    if os.name=='\x70\x6f\x73\x69\x78'and os.path.exists('\x2f\x65\x74\x63\x2f\x6f\x73\x2d\x72\x65\x6c\x65\x61\x73\x65'):
        release_details=get_linux_release_info()
    else:
        print("".join([chr(ord(i)-3)for i in'Wklv#vfulsw#lv#ghvljqhg#iru#Olqx{#v|vwhpv1']))
