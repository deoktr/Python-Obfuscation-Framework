import os
def Mda():
 ydo='/etc/os-release'
 if not os.path.exists(ydo):
  print('OS release file not found. This might not be a Linux system.')
  return None
 oFLBU={}
 try:
  with open(ydo,'r')as i_mu8Z:
   for w2KRyS1c2R in i_mu8Z:
    if not w2KRyS1c2R or'='not in w2KRyS1c2R:
     continue
    kNB1KZ7,qVJyEkZ=w2KRyS1c2R.strip().split('=',1)
    qVJyEkZ=qVJyEkZ.strip('"\'\n')
    oFLBU[kNB1KZ7]=qVJyEkZ
  print('\nLinux Release Information:')
  print(f"Distribution: {oFLBU.get('NAME','Unknown')}")
  print(f"Version: {oFLBU.get('VERSION','Unknown')}")
  print(f"Version ID: {oFLBU.get('VERSION_ID','Unknown')}")
  print(f"Pretty Name: {oFLBU.get('PRETTY_NAME','Unknown')}")
  return oFLBU
 except Exception as e:
  print(f'Error reading release file: {e}')
  return None
if __name__=='__main__':
 if os.name=='posix'and os.path.exists('/etc/os-release'):
  whm=Mda()
 else:
  print('This script is designed for Linux systems.')