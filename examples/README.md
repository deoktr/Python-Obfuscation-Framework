# POF examples

In this directory you'll find 2 files, the source and then generator file. The source file `source.py` contains the Python source file to obfuscate, and the generator file `gen.py` contain the obfuscator code. All outputs are produce to the `out/` directory.

This is useful to test pof, get a feel for the Python API, and how to use it, but also with some outputs and test the result.

Note that you'll need to install pof first.

## Verify

You can verify that the obfuscated outputs are valid by just running them:

```bash
python3 basic.py
# ...

python3 custom_complete.py
# ...

# NOTE: this one may fail if you trigger the evasion, so this is normal
python3 evasion_basic.py
# ...
```

Or you can verify by running every output files:

```bash
./run_all.sh
# ...
```
