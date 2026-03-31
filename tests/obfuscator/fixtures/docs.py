# DocstringObfuscator
from base64 import b64decode


class L8EU:
    """cHJpbnQoIkhlbGxvLCB3b3JsZCEiKQo="""

    pass


exec(b64decode("".join([L8EU.__doc__]).replace("\\n", "")))
