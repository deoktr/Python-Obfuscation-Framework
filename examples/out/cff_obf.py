import os

def get_linux_release_info():
    _state=851
    _ret=None
    while _state!=370:
        if _state==453:
            if not os.path.exists(release_file):
                print('OS release file not found. This might not be a Linux system.')
                return None
            _state=155
        elif _state==962:
            release_file='/etc/os-release'
            _state=453
        elif _state==155:
            release_info={}
            _state=757
        elif _state==757:
            try:
                with open(release_file,'r')as f:
                    for line in f:
                        if not line or'='not in line:
                            continue
                        key,value=line.strip().split('=',1)
                        value=value.strip('"\'\n')
                        release_info[key]=value
                print('\nLinux Release Information:')
                print(f"Distribution: {release_info.get('NAME','Unknown')}")
                print(f"Version: {release_info.get('VERSION','Unknown')}")
                print(f"Version ID: {release_info.get('VERSION_ID','Unknown')}")
                print(f"Pretty Name: {release_info.get('PRETTY_NAME','Unknown')}")
                return release_info
            except Exception as e:
                print(f'Error reading release file: {e}')
                return None
            _state=370
        elif _state==851:
            'Get Linux release info from /etc/os-release.'
            _state=962
    return _ret
if __name__=='__main__':
    if os.name=='posix'and os.path.exists('/etc/os-release'):
        release_details=get_linux_release_info()
    else:
        print('This script is designed for Linux systems.')
