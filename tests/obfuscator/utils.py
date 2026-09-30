import contextlib
import io


def exec_capture(code, a=None):
    output = io.StringIO()

    with contextlib.redirect_stdout(output):
        exec(code, a)

    return output.getvalue()
