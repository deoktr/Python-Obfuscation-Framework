import os

def Tfju3yFpyg():
    """Get Linux release info from /etc/os-release."""
    r86mYpS = '/etc/os-release'
    if not os.path.exists(r86mYpS):
        print('OS release file not found. This might not be a Linux system.')
        return None
    RzHbgjXjps = {}
    try:
        with open(r86mYpS, 'r') as lrv21In9:
            for Vdw7DOdWT in lrv21In9:
                if not Vdw7DOdWT or '=' not in Vdw7DOdWT:
                    continue
                Vj3RKRxY, QSCqeex1P1 = Vdw7DOdWT.strip().split('=', 1)
                QSCqeex1P1 = QSCqeex1P1.strip('"\'\n')
                RzHbgjXjps[Vj3RKRxY] = QSCqeex1P1
        print('\nLinux Release Information:')
        print(f"Distribution: {RzHbgjXjps.get('NAME', 'Unknown')}")
        print(f"Version: {RzHbgjXjps.get('VERSION', 'Unknown')}")
        print(f"Version ID: {RzHbgjXjps.get('VERSION_ID', 'Unknown')}")
        print(f"Pretty Name: {RzHbgjXjps.get('PRETTY_NAME', 'Unknown')}")
        return RzHbgjXjps
    except Exception as HzWN:
        print(f'Error reading release file: {HzWN}')
        return None
if __name__ == '__main__':
    if os.name == 'posix' and os.path.exists('/etc/os-release'):
        LLXDw8F = Tfju3yFpyg()
    else:
        print('This script is designed for Linux systems.')