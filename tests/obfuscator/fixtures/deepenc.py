# DeepEncryptionObfuscator
from base64 import b64decode


def foo():
    r_dict = globals().copy()
    r_dict.update(locals())
    exec(b64decode(b"cHJpbnQgKCJIZWxsbywgd29ybGQiKQoK"), r_dict)
    if "r" not in r_dict:
        return None
    else:
        r_val = r_dict["r"]
        del r_dict
        return r_val


foo()
