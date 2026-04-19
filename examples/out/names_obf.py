import os

def KBWGU6():
    """Get Linux release info from /etc/os-release."""
    zaeKcrMaMC = '/etc/os-release'
    if not os.path.exists(zaeKcrMaMC):
        print('OS release file not found. This might not be a Linux system.')
        return None
    ucJtme = {}
    try:
        with open(zaeKcrMaMC, 'r') as wtrHUFDGMl:
            for KBjP0w_mM in wtrHUFDGMl:
                if not KBjP0w_mM or '=' not in KBjP0w_mM:
                    continue
                UWk, XQS = KBjP0w_mM.strip().split('=', 1)
                XQS = XQS.strip('"\'\n')
                ucJtme[UWk] = XQS
        print('\nLinux Release Information:')
        print(f"Distribution: {ucJtme.get('NAME', 'Unknown')}")
        print(f"Version: {ucJtme.get('VERSION', 'Unknown')}")
        print(f"Version ID: {ucJtme.get('VERSION_ID', 'Unknown')}")
        print(f"Pretty Name: {ucJtme.get('PRETTY_NAME', 'Unknown')}")
        return ucJtme
    except Exception as ApDbWgNfO:
        print(f'Error reading release file: {ApDbWgNfO}')
        return None
if __name__ == '__main__':
    if os.name == 'posix' and os.path.exists('/etc/os-release'):
        uCtgY = KBWGU6()
    else:
        print('This script is designed for Linux systems.')