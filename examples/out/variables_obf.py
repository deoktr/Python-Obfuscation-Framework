import os

def get_linux_release_info():
    """Get Linux release info from /etc/os-release."""
    WpiYdpFP = '/etc/os-release'
    if not os.path.exists(WpiYdpFP):
        print('OS release file not found. This might not be a Linux system.')
        return None
    aYOaQ9e = {}
    try:
        with open(WpiYdpFP, 'r') as wlPfmDfY2_:
            for YfcOwCdJ0 in wlPfmDfY2_:
                if not YfcOwCdJ0 or '=' not in YfcOwCdJ0:
                    continue
                I1IEd, hWRp = YfcOwCdJ0.strip().split('=', 1)
                hWRp = hWRp.strip('"\'\n')
                aYOaQ9e[I1IEd] = hWRp
        print('\nLinux Release Information:')
        print(f"Distribution: {aYOaQ9e.get('NAME', 'Unknown')}")
        print(f"Version: {aYOaQ9e.get('VERSION', 'Unknown')}")
        print(f"Version ID: {aYOaQ9e.get('VERSION_ID', 'Unknown')}")
        print(f"Pretty Name: {aYOaQ9e.get('PRETTY_NAME', 'Unknown')}")
        return aYOaQ9e
    except Exception as e:
        print(f'Error reading release file: {e}')
        return None
if __name__ == '__main__':
    if os.name == 'posix' and os.path.exists('/etc/os-release'):
        V9Psv = get_linux_release_info()
    else:
        print('This script is designed for Linux systems.')