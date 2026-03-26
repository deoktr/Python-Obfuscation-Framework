import random
from datetime import datetime

from pof import Obfuscator, evasion, obfuscator
from pof.utils import generator


def obfuscation_helper(tokens, form, key, obfuscation_class):
    value = form.get(key)
    if value:
        tokens = obfuscation_class(value).obfuscate_tokens(tokens)
    return tokens


def obfuscation_bool_helper(tokens, form, key, obfuscation_class, **kwargs):
    if form.get(key) == "true":
        tokens = obfuscation_class(**kwargs).obfuscate_tokens(tokens)
    return tokens


# TODO (deoktr): multualy exclusive comppressions/crypto/encoding
def add_obfuscation(tokens, form):
    # TODO (deoktr): make the generator customizable from frontend
    gen_dict = {
        86: generator.AdvancedGenerator.realistic_generator(),
        10: generator.BasicGenerator.alphabet_generator(),
        4: generator.BasicGenerator.number_name_generator(length=random.randint(2, 5)),
    }
    gen = generator.AdvancedGenerator.multi_generator(gen_dict)

    # remove
    tokens = obfuscation_bool_helper(
        tokens,
        form,
        "obf_comments",
        obfuscator.CommentsObfuscator,
    )
    tokens = obfuscation_bool_helper(
        tokens,
        form,
        "obf_exceptions",
        obfuscator.ExceptionObfuscator,
    )
    tokens = obfuscation_bool_helper(
        tokens,
        form,
        "obf_change_exceptions",
        obfuscator.ExceptionObfuscator,
        add_codes=True,
        generator=gen,
    )
    tokens = obfuscation_bool_helper(
        tokens,
        form,
        "obf_logging",
        obfuscator.LoggingObfuscator,
    )
    tokens = obfuscation_bool_helper(
        tokens,
        form,
        "obf_logging_remove",
        obfuscator.LoggingRemoveObfuscator,
    )
    tokens = obfuscation_bool_helper(
        tokens,
        form,
        "obf_print",
        obfuscator.PrintObfuscator,
    )

    # control flow
    tokens = obfuscation_bool_helper(
        tokens,
        form,
        "obf_cff",
        obfuscator.ControlFlowFlattenObfuscator,
    )
    tokens = obfuscation_bool_helper(
        tokens,
        form,
        "obf_dead_code",
        obfuscator.DeadCodeObfuscator,
    )

    # rename/move
    tokens = obfuscation_bool_helper(
        tokens,
        form,
        "obf_globals",
        obfuscator.GlobalsObfuscator,
    )
    tokens = obfuscation_bool_helper(
        tokens,
        form,
        "obf_builtins",
        obfuscator.BuiltinsObfuscator,
    )
    tokens = obfuscation_bool_helper(
        tokens,
        form,
        "obf_constants",
        obfuscator.ConstantsObfuscator,
        generator=gen,
        obf_string_rate=0,  # there is some sort of bugs with string
    )
    tokens = obfuscation_bool_helper(
        tokens,
        form,
        "obf_definitions",
        obfuscator.DefinitionsObfuscator,
    )
    tokens = obfuscation_bool_helper(
        tokens,
        form,
        "obf_extract_variables",
        obfuscator.ExtractVariablesObfuscator,
    )

    # some obfuscators should be ran once more here
    tokens = obfuscation_bool_helper(
        tokens,
        form,
        "obf_imports",
        obfuscator.ImportsObfuscator,
    )

    # classic
    tokens = obfuscation_bool_helper(
        tokens,
        form,
        "obf_variables",
        obfuscator.VariablesObfuscator,
        generator=gen,
    )
    tokens = obfuscation_bool_helper(
        tokens,
        form,
        "obf_names",
        obfuscator.NamesObfuscator,
        generator=gen,
    )
    # tokens = obfuscation_bool_helper(
    #     tokens,
    #     form,
    #     "obf_names_rope",
    #     obfuscator.NamesRopeObfuscator,
    # )

    # run all classic string and numbers obfuscators 3 times in a row
    tokens = obfuscation_bool_helper(
        tokens,
        form,
        "obf_string",
        obfuscator.StringsObfuscator,
        import_b64decode=True,
        import_b85decode=True,
    )
    for _ in range(3):
        tokens = obfuscation_bool_helper(
            tokens,
            form,
            "obf_string",
            obfuscator.StringsObfuscator,
            import_b64decode=False,
            import_b85decode=False,
        )
        tokens = obfuscation_bool_helper(
            tokens,
            form,
            "obf_number",
            obfuscator.NumberObfuscator,
        )
        tokens = obfuscation_bool_helper(
            tokens,
            form,
            "obf_boolean",
            obfuscator.BooleanObfuscator,
        )

    # unusual
    tokens = obfuscation_bool_helper(
        tokens,
        form,
        "obf_docstrings",
        obfuscator.DocstringObfuscator,
    )
    tokens = obfuscation_bool_helper(
        tokens,
        form,
        "obf_call",
        obfuscator.CallObfuscator,
    )
    tokens = obfuscation_bool_helper(
        tokens,
        form,
        "obf_imports",
        obfuscator.ImportsObfuscator,
    )
    tokens = obfuscation_bool_helper(
        tokens,
        form,
        "obf_doc",
        obfuscator.CharFromDocObfuscator,
    )
    tokens = obfuscation_bool_helper(
        tokens,
        form,
        "obf_tokens",
        obfuscator.TokensObfuscator,
    )

    # compression
    tokens = obfuscation_bool_helper(tokens, form, "obf_bz2", obfuscator.Bz2Obfuscator)
    tokens = obfuscation_bool_helper(
        tokens,
        form,
        "obf_gzip",
        obfuscator.GzipObfuscator,
    )
    tokens = obfuscation_bool_helper(
        tokens,
        form,
        "obf_lzma",
        obfuscator.LzmaObfuscator,
    )
    tokens = obfuscation_bool_helper(
        tokens,
        form,
        "obf_zlib",
        obfuscator.ZlibObfuscator,
    )

    # ciphers
    tokens = obfuscation_bool_helper(
        tokens,
        form,
        "obf_deepencryption",
        obfuscator.DeepEncryptionObfuscator,
    )
    tokens = obfuscation_bool_helper(tokens, form, "obf_rc4", obfuscator.RC4Obfuscator)
    # TODO (deoktr): fix
    # tokens = obfuscation_bool_helper(
    #     tokens,
    #     form,
    #     "obf_shift",
    #     obfuscator.ShiftObfuscator,
    # )
    tokens = obfuscation_bool_helper(tokens, form, "obf_xor", obfuscator.XORObfuscator)

    # encodings
    tokens = obfuscation_bool_helper(
        tokens,
        form,
        "obf_a85",
        obfuscator.ASCII85Obfuscator,
    )
    tokens = obfuscation_bool_helper(
        tokens,
        form,
        "obf_b16",
        obfuscator.Base16Obfuscator,
    )
    tokens = obfuscation_bool_helper(
        tokens,
        form,
        "obf_b32",
        obfuscator.Base32Obfuscator,
    )
    tokens = obfuscation_bool_helper(
        tokens,
        form,
        "obf_b32hex",
        obfuscator.Base32HexObfuscator,
    )
    tokens = obfuscation_bool_helper(
        tokens,
        form,
        "obf_b64",
        obfuscator.Base64Obfuscator,
    )
    tokens = obfuscation_bool_helper(
        tokens,
        form,
        "obf_b85",
        obfuscator.Base85Obfuscator,
    )
    tokens = obfuscation_bool_helper(
        tokens,
        form,
        "obf_binascii",
        obfuscator.BinasciiObfuscator,
    )
    tokens = obfuscation_bool_helper(
        tokens,
        form,
        "obf_snt",
        obfuscator.SpacenTabObfuscator,
    )
    # UPDATE FIRST
    # tokens = obfuscation_bool_helper(
    #     tokens,
    #     form,
    #     "obf_whitespace",
    #     obfuscator.WhitespaceObfuscator,
    # )
    tokens = obfuscation_bool_helper(
        tokens,
        form,
        "obf_ipv6encoding",
        obfuscator.IPv6Obfuscator,
    )
    tokens = obfuscation_bool_helper(
        tokens,
        form,
        "obf_macencoding",
        obfuscator.MACObfuscator,
    )
    tokens = obfuscation_bool_helper(
        tokens,
        form,
        "obf_uuidencoding",
        obfuscator.UUIDObfuscator,
    )

    # finish
    tokens = obfuscation_bool_helper(
        tokens,
        form,
        "obf_add_comments",
        obfuscator.AddCommentsObfuscator,
    )
    tokens = obfuscation_bool_helper(
        tokens,
        form,
        "obf_add_newlines",
        obfuscator.AddNewlinesObfuscator,
    )
    tokens = obfuscation_bool_helper(
        tokens,
        form,
        "obf_indents",
        obfuscator.IndentsObfuscator,
    )
    tokens = obfuscation_bool_helper(
        tokens,
        form,
        "obf_newline",
        obfuscator.NewlineObfuscator,
    )
    return tokens  # noqa: RET504


def evasion_helper(tokens, form, key, evasion_class):
    value = form.get(key)
    if value:
        tokens = evasion_class(value).add_evasion(tokens)
    return tokens


def evasion_list_helper(tokens, form, key, evasion_class):
    value = form.get(key)
    if value:
        tokens = evasion_class(value.split(",")).add_evasion(tokens)
    return tokens


def evasion_bool_helper(tokens, form, key, evasion_class):
    if form.get(key) == "true":
        tokens = evasion_class().add_evasion(tokens)
    return tokens


def evasion_datetime_helper(tokens, form, key, evasion_class):
    value = form.get(key)
    if value:
        parsed_date = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")  # noqa: DTZ007
        tokens = evasion_class(parsed_date).add_evasion(tokens)
    return tokens


def add_evasion(tokens, form):
    tokens = evasion_helper(tokens, form, "eva_cpu_count_min", evasion.CPUCountEvasion)
    tokens = evasion_bool_helper(
        tokens,
        form,
        "eva_tracemalloc",
        evasion.TracemallocEvasion,
    )
    tokens = evasion_bool_helper(tokens, form, "eva_debugger", evasion.DebuggerEvasion)
    tokens = evasion_bool_helper(
        tokens,
        form,
        "eva_executable_path",
        evasion.ExecPathEvasion,
    )
    tokens = evasion_helper(tokens, form, "eva_exec_method", evasion.ExecMethodEvasion)
    tokens = evasion_helper(tokens, form, "eva_domain", evasion.DomainEvasion)
    tokens = evasion_helper(tokens, form, "eva_hostname", evasion.HostnameEvasion)
    tokens = evasion_helper(tokens, form, "eva_linux_uid", evasion.LinuxUIDEvasion)
    tokens = evasion_helper(tokens, form, "eva_username", evasion.UsernameEvasion)
    tokens = evasion_helper(
        tokens,
        form,
        "eva_linux_proc_count",
        evasion.LinuxProcCountEvasion,
    )
    tokens = evasion_list_helper(
        tokens,
        form,
        "eva_directory_exist",
        evasion.DirectoryListExistEvasion,
    )
    tokens = evasion_list_helper(
        tokens,
        form,
        "eva_directory_missing",
        evasion.DirectoryListMissingEvasion,
    )
    tokens = evasion_list_helper(tokens, form, "eva_argv", evasion.ArgvEvasion)
    tokens = evasion_list_helper(
        tokens,
        form,
        "eva_file_exist",
        evasion.FileListExistEvasion,
    )
    tokens = evasion_list_helper(
        tokens,
        form,
        "eva_file_missing",
        evasion.FileListMissingEvasion,
    )
    tokens = evasion_helper(tokens, form, "eva_tmp", evasion.TmpCountEvasion)
    tokens = evasion_helper(
        tokens,
        form,
        "eva_linux_ram_count",
        evasion.LinuxRAMCountEvasion,
    )
    # TODO (deoktr): convert to multile argumnets, or have multiple form fields?
    tokens = evasion_bool_helper(
        tokens,
        form,
        "eva_windows_prompt",
        evasion.WinPromptEvasion,
    )
    tokens = evasion_datetime_helper(tokens, form, "eva_expire", evasion.ExpireEvasion)
    tokens = evasion_helper(
        tokens,
        form,
        "eva_linux_uptime",
        evasion.LinuxUptimeEvasion,
    )
    tokens = evasion_bool_helper(tokens, form, "eva_utc_evasion", evasion.UTCEvasion)
    return tokens  # noqa: RET504


class HtmlFormObfuscator(Obfuscator):
    def run(self, source, form) -> str:
        tokens = self._get_tokens(source)
        tokens = add_evasion(tokens, form)
        tokens = add_obfuscation(tokens, form)
        return self._untokenize(tokens)


obfuscator_instance = HtmlFormObfuscator()
