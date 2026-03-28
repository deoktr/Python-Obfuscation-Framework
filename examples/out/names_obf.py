import os

def YxshfcTU():
    """Get Linux release info from /etc/os-release."""
    IqT = '/etc/os-release'
    if not os.path.exists(IqT):
        print('OS release file not found. This might not be a Linux system.')
        return None
    lVO = {}
    try:
        with open(IqT, 'r') as y0G6JJHxPy:
            for jMpue in y0G6JJHxPy:
                if not jMpue or '=' not in jMpue:
                    continue
                jB68Fqo7, w2nXO4CRV7 = jMpue.strip().split('=', 1)
                w2nXO4CRV7 = w2nXO4CRV7.strip('"\'\n')
                lVO[jB68Fqo7] = w2nXO4CRV7
        print('\nLinux Release Information:')
        print(f"Distribution: {lVO.get('NAME', 'Unknown')}")
        print(f"Version: {lVO.get('VERSION', 'Unknown')}")
        print(f"Version ID: {lVO.get('VERSION_ID', 'Unknown')}")
        print(f"Pretty Name: {lVO.get('PRETTY_NAME', 'Unknown')}")
        return lVO
    except Exception as MjaN:
        print(f'Error reading release file: {MjaN}')
        return None
if __name__ == '__main__':
    if os.name == 'posix' and os.path.exists('/etc/os-release'):
        vsvrGxu5 = YxshfcTU()
    else:
        print('This script is designed for Linux systems.')