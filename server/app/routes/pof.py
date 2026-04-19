# POF, a free and open source Python obfuscation framework.
# Copyright (C) 2022 - 2026  Deoktr
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import logging

from flask import Blueprint, current_app, request
from markupsafe import escape
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import PythonLexer

from app.obfuscate import obfuscator_instance

from pof.utils.format import black_format

logger = logging.getLogger(__name__)

pof_bp = Blueprint("pof", __name__)


@pof_bp.post("/")
def pof_route():
    """Basic HTTP endpoint to send and receive raw source code."""
    src = request.get_data().decode()
    if len(src) > current_app.config["INPUT_SIZE_LIMIT"]:
        logger.warning("input too large")
        return "Inpt too large", 413

    try:
        return obfuscator_instance.obfuscate(src)
    except Exception:
        logger.exception("failed to obfuscate")
        return "", 500


def format_html_error(msg: str) -> str:
    return f'<p class="error">{msg}</p>'


@pof_bp.post("/html")
def pof_route_html():
    """HTML endpoint to send form data and receive HTML formatted code."""
    src = request.form.get("src", "")
    if len(src) > current_app.config["INPUT_SIZE_LIMIT"]:
        logger.warning("input too large")
        return format_html_error("Input too large.")

    try:
        obf = obfuscator_instance.run(src, request.form)
    except Exception:
        logger.exception("failed to obfuscate")
        return format_html_error("Failed to obfuscate, invalid input.")

    if (
        current_app.config["ENABLE_BLACK_FORMAT"]
        and request.form.get("format_black", "false") == "true"
    ):
        try:
            obf = black_format(obf)
        except Exception:
            logger.exception("failed to format with black")

    if current_app.config["ENABLE_PYGMENT"]:
        try:
            return highlight(
                obf,
                PythonLexer(),
                HtmlFormatter(cssstyles="background: none;"),
            )
        except Exception:
            logger.exception("failed to highlight")

            # in case we fail to highlight, return non highlighted version
            return f'<p style="white-space: pre-wrap;">{escape(obf)}</p>'
    else:
        return f'<p style="white-space: pre-wrap;">{escape(obf)}</p>'
