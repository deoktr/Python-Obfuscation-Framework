import os

def bJFC():
    Vnl3e = '/etc/os-release'
    if not os.path.exists(Vnl3e):
        print('OS release file not found. This might not be a Linux system.')
        return None
    fBD = {}
    try:
        with open(Vnl3e, 'r') as Jz2:
            for CJau3R in Jz2:
                if not CJau3R or '=' not in CJau3R:
                    continue
                jBRnlWm, wHf7pWkL = CJau3R.strip().split('=', 1)
                wHf7pWkL = wHf7pWkL.strip('"\'\n')
                fBD[jBRnlWm] = wHf7pWkL
        print('\nLinux Release Information:')
        print(f"Distribution: {fBD.get('NAME', 'Unknown')}")
        print(f"Version: {fBD.get('VERSION', 'Unknown')}")
        print(f"Version ID: {fBD.get('VERSION_ID', 'Unknown')}")
        print(f"Pretty Name: {fBD.get('PRETTY_NAME', 'Unknown')}")
        return fBD
    except Exception as KyifDLkD:
        print(f'Error reading release file: {KyifDLkD}')
        return None
if __name__ == '__main__':
    if os.name == 'posix' and os.path.exists('/etc/os-release'):
        yJ7U = bJFC()
    else:
        print('This script is designed for Linux systems.')