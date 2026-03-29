# ASCII85Obfuscator
from base64 import a85decode
exec(a85decode('E,oZ1F=8M-ASc1$/0K.TEbo86.1-'))

# Base16Obfuscator
from base64 import b16decode
exec(b16decode('7072696E74282748656C6C6F2C20776F726C6427290A'))

# Base32Obfuscator
from base64 import b32decode
exec(b32decode('OBZGS3TUFATUQZLMNRXSYIDXN5ZGYZBHFEFA===='))

# Base32HexObfuscator
from base64 import b32hexdecode
exec(b32hexdecode('E1P6IRJK50JKGPBCDHNIO83NDTP6OP175450===='))

# Base64Obfuscator
from base64 import b64decode
exec(b64decode('cHJpbnQoJ0hlbGxvLCB3b3JsZCcpCg=='))

# Base85Obfuscator
from base64 import b85decode
exec(b85decode('aB^vGbSNiCWo&G3EFgDpa%^NLDGC'))

# BinasciiObfuscator
import binascii,marshal
exec(marshal.loads(binascii.a2b_base64( b'8xYAAABwcmludCgnSGVsbG8sIHdvcmxkJykK\n')))

# TokensObfuscator
from tokenize import untokenize
exec(untokenize([(1,'print'),(54,'('),(3,"'Hello, world'"),(54,')'),(4,'\n'),(0,''),]))

# IPv6Obfuscator
import binascii
exec(binascii.a2b_hex(''.join(['7072:696e:7428:2748:656c:6c6f:2c20:776f','726c:6427:290a:1000:0000:0000:0000:0000',]).replace(':','').strip('0')[:-1]))

# MACObfuscator
import binascii
exec(binascii.a2b_hex(''.join(['70-72-69-6e-74-28','27-48-65-6c-6c-6f','2c-20-77-6f-72-6c','64-27-29-0a-10-00',]).replace('-','').strip('0')[:-1]))

# UUIDObfuscator
exec(binascii.a2b_hex("".join(['7072696e-7428-2748-656c-6c6f2c20776f','726c6427-290a-1000-0000-000000000000',]).replace("-","").strip('0')[:-1]))
