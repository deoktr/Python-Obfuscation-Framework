/*
* YARA rules to identify Python obfuscation and malware from source code.
* Designed for use with pof (Python Obfuscation Framework) output detection.
*
* Confidence levels:
*   high   - Pattern almost never appears in legitimate code
*   medium - Pattern can appear legitimately but is suspicious in combination
*   low    - Common indicator; useful for triage, not standalone alerts
*/

rule execFunction
{
    meta:
        description = "Function `exec` used multiple times"
        author = "deoktr"
        confidence = "low"

    strings:
        $exec = "exec("

    condition:
        #exec > 2
}

rule suspiciousImports
{
    meta:
        description = "Suspicious library imports commonly used in obfuscation"
        author = "deoktr"
        confidence = "low"

    strings:
        $base64 = "import base64"
        $base64from = "from base64 import b64decode"
        $base85 = "from base64 import b85decode"
        $marshal = "import marshal"
        $codecs = "import codecs"
        $binascii = "import binascii"
        $tokenize = "from tokenize import untokenize"

    condition:
        any of them
}

rule obfuscationOxyry
{
    meta:
        description = "Obfuscation using Oxyry (now closed)"
        author = "deoktr"
        confidence = "high"

    strings:
        $varialbes = /O[O0]{16}/

    condition:
        all of them
}

rule LOTLURL
{
    meta:
        description = "Living Off Trusted Sites URLs"
        author = "deoktr"
        confidence = "medium"
        resources = "https://lots-project.com/"

    strings:
        $githubusercontent = "githubusercontent"
        $github = "github"
        $pastebin = "pastebin"
        $pasters = "paste.rs"
        $cl1pnet = "cl1p.net"

    condition:
        any of them
}

rule zerowidthspace
{
    meta:
        description = "Whitespace encoding with zero width spaces"
        author = "deoktr"
        confidence = "high"

    strings:
        $a = "\xe2\x80\x8b"

    condition:
        any of them
}

rule compressionExecMarshal
{
    meta:
        description = "Compression obfuscation: marshal.loads + decompress + exec (Bz2, Gzip, Lzma, Zlib)"
        author = "deoktr"
        confidence = "high"

    strings:
        $marshal = "marshal.loads("
        $bz2 = "bz2.decompress("
        $gzip = "gzip.decompress("
        $lzma = "lzma.decompress("
        $zlib = "zlib.decompress("
        $exec = "exec("

    condition:
        $exec and $marshal and ($bz2 or $gzip or $lzma or $zlib)
}

rule builtinsManipulation
{
    meta:
        description = "Builtins obfuscation: accessing builtins via __dict__ or __getattribute__"
        author = "deoktr"
        confidence = "high"
        obfuscator = "BuiltinsObfuscator"

    strings:
        $dict_access = "__builtins__.__dict__["
        $getattr = "__builtins__.__getattribute__("
        $getitem = "__builtins__.__dict__.__getitem__("
        $globals_builtins = "globals()['__builtins__'].__dict__["

    condition:
        any of them
}

// NOTE: this is only the default names, they can be changed with obfuscators
rule cipherRC4
{
    meta:
        description = "RC4 cipher obfuscation: RC4 decrypt function with exec"
        author = "deoktr"
        confidence = "high"
        obfuscator = "RC4Obfuscator"

    strings:
        $rc4decrypt = "rc4decrypt("
        $ksa = "def KSA("
        $prga = "def PRGA("
        $exec = "exec("

    condition:
        $exec and ($rc4decrypt or ($ksa and $prga))
}

rule cipherShiftExec
{
    meta:
        description = "Shift cipher obfuscation: exec with chr(ord()) shift pattern"
        author = "deoktr"
        confidence = "high"
        obfuscator = "ShiftObfuscator"

    strings:
        $pattern = /exec\(""\s*\.join\(\[chr\(ord\(/

    condition:
        any of them
}

rule cipherXOR
{
    meta:
        description = "XOR cipher obfuscation: XOR decrypt function with exec"
        author = "deoktr"
        confidence = "medium"
        obfuscator = "XORObfuscator"

    strings:
        $decrypt_func = /def decrypt\s*\(\s*cipher\s*,\s*key\s*\)/
        $bytearray = "bytearray("
        $xor = /\^\s*(key|next\(keystream\))/
        $exec = "exec("

    condition:
        $exec and $bytearray and ($decrypt_func or $xor)
}

rule encodingExec
{
    meta:
        description = "Encoding obfuscation: exec + base16/32/32hex/ascii85 decode"
        author = "deoktr"
        confidence = "high"
        obfuscator = "Base16Obfuscator, Base32Obfuscator, Base64Obfuscator, Base85Obfuscator, ASCII85Obfuscator"

    strings:
        $exec_b64 = "exec(b64decode("
        $exec_b85 = "exec(b85decode("
        $exec_b16 = "exec(b16decode("
        $exec_b32 = "exec(b32decode("
        $exec_b32hex = "exec(b32hexdecode("
        $exec_a85 = "exec(a85decode("

    condition:
        any of them
}

rule encodingExecBinascii
{
    meta:
        description = "Binascii encoding obfuscation: binascii + marshal + exec"
        author = "deoktr"
        confidence = "high"

    strings:
        $binascii = "binascii.a2b_base64("
        $marshal = "marshal.loads("
        $exec = "exec("

    condition:
        $exec and $marshal and $binascii
}

rule steganoAddressExec
{
    meta:
        description = "Steganographic obfuscation: IPv6/MAC/UUID address encoding with exec"
        author = "deoktr"
        confidence = "high"

    strings:
        $a2b_hex = "a2b_hex("
        $exec = "exec("
        $replace_colon = ".replace(':','')"
        $replace_dash = ".replace('-','')"
        $replace_hyphen = /\.replace\(\s*["']-["']\s*,\s*["']["']\s*\)/
        $strip = ".strip('0')"

    condition:
        $exec and $a2b_hex and ($replace_colon or $replace_dash or $replace_hyphen or $strip)
}

rule docstringExec
{
    meta:
        description = "Docstring obfuscation: code hidden in class/function docstrings and executed"
        author = "deoktr"
        confidence = "high"
        obfuscator = "DocstringObfuscator"

    strings:
        $doc = "__doc__"
        $b64decode = "b64decode("
        $exec = "exec("
        $replace = ".replace("

    condition:
        $exec and $b64decode and $doc and $replace
}

rule globalsLookup
{
    meta:
        description = "Globals obfuscation: function calls replaced with globals() dictionary lookups"
        author = "deoktr"
        confidence = "low"
        obfuscator = "GlobalsObfuscator"

    strings:
        $globals = "globals()['"

    condition:
        #globals >= 3
}

rule callObfuscation
{
    meta:
        description = "Call obfuscation: function calls replaced with .__call__() method"
        author = "deoktr"
        confidence = "low"
        obfuscator = "CallObfuscator"

    strings:
        $call = ".__call__("

    condition:
        #call >= 3
}

rule shiftCipherPattern
{
    meta:
        description = "Shift cipher string obfuscation: chr(ord()) character shifting in loops"
        author = "deoktr"
        confidence = "medium"
        obfuscator = "StringsObfuscator"

    strings:
        $pattern = /chr\(ord\(\s*\w+\s*\)\s*[-+]\s*\d+\s*\)/
        $join = /join\(\[/

    condition:
        $pattern and $join
}

rule importObfuscation
{
    meta:
        description = "Import obfuscation: modules loaded via __import__() instead of import statement"
        author = "deoktr"
        confidence = "low"
        obfuscator = "ImportsObfuscator"

    strings:
        $import = "__import__('"

    condition:
        #import >= 3
}

rule deepEncryption
{
    meta:
        description = "pof DeepEncryption: function bodies encrypted with b64 + exec in globals dict"
        author = "deoktr"
        confidence = "high"
        obfuscator = "DeepEncryptionObfuscator"

    strings:
        $globals_copy = "globals().copy()"
        $update_locals = ".update(locals())"
        $exec_b64 = "exec(b64decode("
        $r_dict = "r_dict"

    condition:
        $globals_copy and $update_locals and $exec_b64 and $r_dict
}

rule spacenTabEncoding
{
    meta:
        description = "pof SpacenTab encoding: code hidden in space/tab binary encoding"
        author = "deoktr"
        confidence = "high"
        obfuscator = "WhitespaceObfuscator"

    strings:
        $sntdecode = "def sntdecode("
        $space_replace = /replace\(\s*["'] ["']\s*,\s*["']0["']\s*\)/
        $tab_replace = /replace\(\s*["']\\t["']\s*,\s*["']1["']\s*\)/

    condition:
        $sntdecode or ($space_replace and $tab_replace)
}

rule tokensObfuscation
{
    meta:
        description = "pof Tokens obfuscation: code reconstructed from token tuples via untokenize"
        author = "deoktr"
        confidence = "high"
        obfuscator = "TokensObfuscator"

    strings:
        $import = "from tokenize import untokenize"
        $exec = "exec(untokenize("

    condition:
        $import and $exec
}

rule booleanObfuscation
{
    meta:
        description = "pof Boolean obfuscation: True/False replaced with equivalent expressions"
        author = "deoktr"
        confidence = "medium"
        obfuscator = "BooleanObfuscator"

    strings:
        $all_empty = "all([])"
        $all_nested = "all([[]])"
        $not_not_true = "not not True"
        $not_not_false = "not not False"
        $bool_1 = "bool(1)"
        $bool_0 = "bool(0)"
        $in_empty = "'' in ''"

    condition:
        3 of them
}

rule controlFlowFlatten
{
    meta:
        description = "pof Control flow flattening: sequential code transformed into state-machine dispatch loop"
        author = "pof"
        confidence = "high"
        obfuscator = "ControlFlowFlattenObfuscator"

    strings:
        $state_init = "_state ="
        $dispatch_loop = "while _state !="
        $state_match = /if _state ==|elif _state ==/

    condition:
        all of them
}

rule numberObfuscation
{
    meta:
        description = "pof Number obfuscation: literals replaced with hex conversion, boolean arithmetic, or bitwise operations"
        author = "pof"
        confidence = "high"
        obfuscator = "NumberObfuscator"

    strings:
        $hex_conv = /int\(\s*'0x[0-9a-fA-F]+'\s*,\s*0\s*\)/
        $bool_arith = "(True + True"
        $round_magic = /round\(.+,\s*12\)/

    condition:
        any of them
}

rule stringObfuscationAdvanced
{
    meta:
        description = "pof String obfuscation: string reversal or character filtering patterns"
        author = "pof"
        confidence = "medium"
        obfuscator = "StringsObfuscator"

    strings:
        $reversal = "[::-1]"
        $enumerate_filter = "enumerate("
        $modulo_filter = /\w\s*%\s*\d+\s*==\s*0/

    condition:
        (#reversal > 2) or ($enumerate_filter and $modulo_filter)
}

rule deadCodeInjection
{
    meta:
        description = "pof Dead code injection: unreachable code blocks with obviously false conditions"
        author = "pof"
        confidence = "high"
        obfuscator = "DeadCodeObfuscator"

    strings:
        $if_false = "if False:"
        $while_false = "while False:"
        $while_zero = "while 0:"
        $for_empty_list = /for [a-zA-Z_]+ in \[\]:/
        $for_range_zero = /for [a-zA-Z_]+ in range\(0\):/
        $not_true = "(not True)"
        // Dead function pattern: function defined with random modulo assignments inside
        $dead_func_assign = /def [a-zA-Z_][a-zA-Z0-9_]*\([a-zA-Z_][a-zA-Z0-9_]*\):\n\s+[a-zA-Z_][a-zA-Z0-9_]*=\d+%\d+/

    condition:
        any of them
}

rule constantsExtraction
{
    meta:
        description = "pof Constants extraction: builtin functions reassigned to short variable names"
        author = "pof"
        confidence = "medium"
        obfuscator = "ConstantsObfuscator"

    strings:
        $builtin_len = /\n[a-zA-Z_][a-zA-Z0-9_]*=len\n/
        $builtin_print = /\n[a-zA-Z_][a-zA-Z0-9_]*=print\n/
        $builtin_int = /\n[a-zA-Z_][a-zA-Z0-9_]*=int\n/
        $builtin_str = /\n[a-zA-Z_][a-zA-Z0-9_]*=str\n/
        $builtin_type = /\n[a-zA-Z_][a-zA-Z0-9_]*=type\n/
        $builtin_range = /\n[a-zA-Z_][a-zA-Z0-9_]*=range\n/
        $builtin_list = /\n[a-zA-Z_][a-zA-Z0-9_]*=list\n/
        $builtin_dict = /\n[a-zA-Z_][a-zA-Z0-9_]*=dict\n/

    condition:
        3 of them
}

rule exceptionMessageStrip
{
    meta:
        description = "pof Exception obfuscation: error messages stripped from raise statements"
        author = "pof"
        confidence = "medium"
        obfuscator = "ExceptionObfuscator"

    strings:
        $exc_empty_error = /raise [A-Z][a-zA-Z]*Error\(\)/
        $exc_empty_exception = "raise Exception()"
        $exc_empty_warning = /raise [A-Z][a-zA-Z]*Warning\(\)/

    condition:
        #exc_empty_error + #exc_empty_exception + #exc_empty_warning >= 2
}
