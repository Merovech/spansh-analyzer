"""
Logging utility to be able to control when a message overwrites a previous one on the
same line or is printed on a new line.
"""

import re
import shutil
from colorama import init, Fore, Style

init(autoreset=False)

_COLORS = {
    "OK":    Fore.GREEN,
    "WARN":  Fore.YELLOW,
    "ERROR": Fore.RED,
}
_TAG_RE = re.compile(r"\[(OK|WARN|ERROR)\]")

_verbose: bool = False


def set_verbose(enabled: bool) -> None:
    """Enable or disable verbose logging."""
    global _verbose
    _verbose = enabled


def write(msg: str, color: str = "") -> None:
    """Writes a message to the console without a newline at the end."""
    write_internal(msg, False, color)


def writeln(msg: str, color: str = "") -> None:
    """Writes a message to the console with a newline at the end."""
    write_internal(msg, True, color)


def verbose_writeln(msg: str, color: str = "") -> None:
    """Writes a message only when verbose logging is enabled."""
    if _verbose:
        write_internal(msg, True, color)


def _colorize(msg: str) -> str:
    """Replace [OK], [WARN], [ERROR] with their colorized equivalents."""
    def replace(m: re.Match) -> str:
        tag = m.group(1)
        return f"[{_COLORS[tag]}{tag}{Style.RESET_ALL}]"
    return _TAG_RE.sub(replace, msg)


def write_internal(msg: str, last: bool = False, color: str = "") -> None:
    """Overwrite the current terminal line with msg.  If last=True, end with a newline."""
    terminal_size = shutil.get_terminal_size().columns
    colored_msg = f"{color}{_colorize(msg)}{Style.RESET_ALL}" if color else _colorize(msg)
    print(f"\r{colored_msg:<{terminal_size}}", end="\n" if last else "", flush=True)

# To do: log to file
