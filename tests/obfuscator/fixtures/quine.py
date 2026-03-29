# QuineStager
from base64 import b64decode
from tokenize import untokenize

esource='cHJpbnQoJ0hlbGxvLCB3b3JsZCcpCg=='
tokens=[(1,'from'),(1,'base64'),(1,'import'),(1,'b64decode'),(4,'\n'),(1,'from'),(1,'tokenize'),(1,'import'),(1,'untokenize'),(4,'\n'),(1,'esource'),(54,'='),(4,'\n'),(1,'tokens'),(54,'='),(4,'\n'),(1,'def'),(1,'quine'),(54,'('),(54,')'),(54,':'),(4,'\n'),(5,' '),(1,'return'),(1,'untokenize'),(54,'('),(1,'tokens'),(54,'['),(54,':'),(2,'12'),(54,']'),(54,')'),(54,'+'),(1,'repr'),(54,'('),(1,'esource'),(54,')'),(54,'+'),(1,'untokenize'),(54,'('),(1,'tokens'),(54,'['),(2,'12'),(54,':'),(2,'15'),(54,']'),(54,')'),(54,'+'),(1,'repr'),(54,'('),(1,'tokens'),(54,')'),(54,'+'),(1,'untokenize'),(54,'('),(1,'tokens'),(54,'['),(2,'15'),(54,':'),(54,']'),(54,')'),(4,'\n'),(6,''),(1,'exec'),(54,'('),(1,'b64decode'),(7,'('),(1,'esource'),(8,')'),(54,')'),(4,'\n')]
def quine():
    return untokenize(tokens[:12])+repr(esource)+untokenize(tokens[12:15])+repr(tokens)+untokenize(tokens[15:])

exec(b64decode(esource))
