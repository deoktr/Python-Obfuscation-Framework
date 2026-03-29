# obfuscated
__builtins__.__getattribute__('print')('Hello, world')

__builtins__.__dict__['print']('Hello, world')

globals()['__builtins__'].__dict__['print']('Hello, world')

__builtins__.__dict__.__getitem__('print')('Hello, world')

print.__call__('Hello, world')

# GlobalsObfuscator
def foo():
    print("foo")

globals()['foo']()

# ShiftObfuscator
exec("".join([chr(ord(i)-3)for i in'sulqw+*Khoor/#zruog*,\r']))

# SpacenTabObfuscator
def sntdecode(encoded):
    msg_bin=encoded.replace(" ","0").replace("\t","1")
    n=int(msg_bin,2)
    return n.to_bytes((n.bit_length()+7)//8,"big")

exec(sntdecode('\t\t\t     \t\t\t  \t  \t\t \t  \t \t\t \t\t\t  \t\t\t \t    \t \t     \t  \t\t\t \t  \t    \t\t  \t \t \t\t \t\t   \t\t \t\t   \t\t \t\t\t\t  \t \t\t    \t      \t\t\t \t\t\t \t\t \t\t\t\t \t\t\t  \t  \t\t \t\t   \t\t  \t    \t  \t\t\t  \t \t  \t    \t \t '))

# WhitespaceObfuscator
def wsdecode(encoded):
    msg_bin=encoded.replace(" ","0").replace('\u200b',"1")
    n=int(msg_bin,2)
    return n.to_bytes((n.bit_length()+7)//8,"big")

exec(wsdecode("​​​     ​​​  ​  ​​ ​  ​ ​​ ​​​  ​​​ ​    ​ ​     ​  ​​​ ​  ​    ​​  ​ ​ ​​ ​​   ​​ ​​   ​​ ​​​​  ​ ​​    ​      ​​​ ​​​ ​​ ​​​​ ​​​  ​  ​​ ​​   ​​  ​    ​  ​​​  ​ ​  ​    ​ ​ "))

# XORObfuscator
from base64 import b64decode

def decrypt(cipher,key):
    bcipher=bytearray(b64decode(cipher))
    text=bytearray()
    ki=0
    for i in bcipher:
        text.append(i^key[ki%len(key)])
        ki+=1
    return text
exec(decrypt(b'RkNfWkAcHnxTXVpbGBROW0RdUhMdPg==', b'61644494').decode())
