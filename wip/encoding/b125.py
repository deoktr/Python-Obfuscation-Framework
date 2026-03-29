# https://github.com/eyaler/ztml/blob/main/ztml/base125.py
"""Base125 encoding based on Base122 and optimized for inline HTML / JS text compression and image encoding.

If we must use utf8 encoding for HTML or JS, crEnc will not work.
Instead, we can use this original and unnecessarily-optimized version of the variable length Base122.
The original byte stream is split into 7 bit chunks,
which are encoded as a single byte: 0xxxxxxx, to comply with utf8 code point scheme.
We only use 125 byte values out of 128 (excluding CR, backslash and `)
and encode the remaining three with a double byte scheme: 110ssxxx 10xxxxxx,
where ss is 01, 10 or 11, and 9 bits are left for next data.
Alternatively, if these are the final 7 bits, we instead encode as: 1100010x 10xxxxxx.
As, we embed in JS template literals quotes ``, we further escape ${ with backslash.
The overhead is ~ 8/7 * 253/256 + 16/11 * 3/256 - 1 ~ 14.7% (compared to 33.3% for Base64).
The decoder further takes care of HTML character override for NUL.
An optimal global character modular offset can be added to minimize escaping, similar to dynEncode (disabled by default).
A minimalistic JS decoder code is generated.

References:
https://en.wikipedia.org/wiki/Binary-to-text_encoding
https://blog.kevinalbs.com/base122
https://github.com/kevinAlbs/Base122
https://github.com/eshaz/simple-yenc#what-is-dynencode
"""

if not __package__:
    import default_vars
else:
    # noinspection PyPackages
    from . import default_vars


illegal = ["", 13, 92, 96]


def encode(data: bytes, offset: int = 0, validate: bool = True) -> bytes:
    cur_index = 0
    cur_bit = 0  # Points to current bit needed
    out = bytearray()

    # Get 7 or 9 bits of input data. Returns None if there is no input left
    def get_bits(length: int) -> int | None:
        nonlocal cur_index, cur_bit
        if cur_index >= len(data):
            return None

        # Shift, mask, unshift to get first part. Align it to a 7 or 9 bit chunk
        first_part = (255 >> cur_bit & data[cur_index] + offset & 255) << cur_bit
        diff = 8 - length
        if diff > 0:
            first_part >>= diff
        else:
            first_part <<= -diff
        # Check if we need to go to the next byte for more bits
        cur_bit += length
        if cur_bit < 8:
            return first_part  # Do not need next byte
        cur_bit -= 8
        cur_index += 1
        # Now we want bits [0..cur_bit] of the next byte if it exists
        if cur_index >= len(data):
            return first_part
        # Align it
        second_part = (
            0xFF00 >> cur_bit & data[cur_index] + offset & 255
        ) >> 8 - cur_bit
        return first_part | second_part

    while True:
        # Grab 7 bits
        bits = get_bits(7)
        if bits is None:
            break
        try:
            illegal_index = illegal.index(bits)
            # Since this will be a two-byte character, get the next chunk of 9 bits
            next_bits = get_bits(9)
            if next_bits is None:
                b1 = 4
                next_bits = bits
            else:
                b1 = illegal_index << 3
            # Push first 3 bits onto first byte, remaining 6 onto second
            out.extend([192 | b1 | next_bits >> 6, 128 | next_bits & 63])
        except ValueError:
            out.append(bits)

    if validate:
        decoded = decode(out, offset)
        assert decoded == data, (len(decoded), len(data), decoded[:30], data[:30])
    return out.replace(b"${", b"\\${")


def optimize_encode(data: bytes, validate: bool = True) -> tuple[bytes, int, int]:
    best_offset = 0
    for offset in range(256):
        length = len(encode(data, offset, validate=False))
        if offset == 0:
            best_length = length0 = length
        if length < best_length:
            best_length = length
            best_offset = offset
    out = encode(data, best_offset, validate)
    return out, best_offset, length0 - best_length


def decode(data: bytes, offset: int = 0) -> bytes:
    out = bytearray()
    next_byte = 0
    k = 0

    def push_bits(bits: int, length: int = 7) -> None:
        nonlocal next_byte, k
        next_byte |= bits << (length < 8) >> k >> (length > 8)
        k += length
        if k > 7:
            out.append((next_byte & 255) - offset & 255)
            k -= 8
            next_byte = bits << 8 - k

    for byte in data.decode():
        b = ord(byte)
        if b > 127:
            ss = b >> 9
            if ss:
                push_bits(illegal[ss])
            push_bits(b << 2 * (not ss) & 511, 9)
        else:
            push_bits(b)
    return out


def get_js_decoder(
    data: bytes,
    offset: int | None = 0,
    output_var: str = default_vars.bytearray,
    validate: bool = True,
) -> bytes:
    if offset is None:
        encoded, offset, saved = optimize_encode(data, validate)  # Time-consuming op.
    else:
        encoded = encode(data, offset, validate)
    illegal_str = ",".join(str(i) for i in illegal)
    first_part = f"""k=n=0
p=(b,l=7)=>(n|=b<<(l<8)>>k>>(l>8),k+=l,k>7?(v=n{-offset or ''},k-=8,n=b<<8-k,v):[])
{output_var}=new Uint8Array([...`"""
    last_part = f"`].flatMap(c=>(i=c.charCodeAt()%65533,i>127?(e=i>>9,[e?p([{illegal_str}][e]):[],p(i<<2*!e&511,9)].flat()):p(i))))\n"
    return first_part.encode() + encoded + last_part.encode()


def test() -> None:
    for i in range(100):
        for j in range(100):
            for offset in [0, 1]:
                for symbol in [b"\r", b"\\", b"`"]:
                    encode(b"\0" * i + symbol * j, offset, validate=True)


if __name__ == "__main__":
    test()
