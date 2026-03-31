import os

def Ray9KtDB_():
    vN_isq = '/etc/os-release'
    if not os.path.exists(vN_isq):
        print('OS release file not found. This might not be a Linux system.')
        return None
    Gti2zkl = {}
    try:
        with open(vN_isq, 'r') as WNWpzI4OgZ:
            for PgQ in WNWpzI4OgZ:
                if not PgQ or '=' not in PgQ:
                    continue
                bz2u5I, IJF = PgQ.strip().split('=', 1)
                IJF = IJF.strip('"\'\n')
                Gti2zkl[bz2u5I] = IJF
        print('\nLinux Release Information:')
        print(f"Distribution: {Gti2zkl.get('NAME', 'Unknown')}")
        print(f"Version: {Gti2zkl.get('VERSION', 'Unknown')}")
        print(f"Version ID: {Gti2zkl.get('VERSION_ID', 'Unknown')}")
        print(f"Pretty Name: {Gti2zkl.get('PRETTY_NAME', 'Unknown')}")
        return Gti2zkl
    except Exception as y7R:
        print(f'Error reading release file: {y7R}')
        return None
if __name__ == '__main__':
    if os.name == 'posix' and os.path.exists('/etc/os-release'):
        XYvmvI = Ray9KtDB_()
    else:
        print('This script is designed for Linux systems.')