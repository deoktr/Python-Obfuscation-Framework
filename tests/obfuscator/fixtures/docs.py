# DocstringObfuscator
from base64 import b64decode
class Foo:
    """
    cHJpbnQoJ0hlbGxvLCB3b3JsZCcpCg==
    """
    pass


exec(b64decode(Foo.__doc__.replace('\n','').replace(' ','')))
