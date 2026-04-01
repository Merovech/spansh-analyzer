"""
Logging utility to be able to control when a message overwrites a previous one on the
same line or is printed on a new line.
"""

import re
import shutil
from colorama import init, Fore, Style
from datetime import datetime
from pathlib import Path

# Initialize colorama and define colors
init(autoreset=False)

_COLORS = {
    "OK":    Fore.GREEN,
    "WARN":  Fore.YELLOW,
    "ERROR": Fore.RED,
}

# Tags to look for when colorizing part of a line automatically
_TAG_RE = re.compile(r"\[(OK|WARN|ERROR)\]")

_verbose: bool = False

# Create the log file
_log_file: Path = Path(f"log-{datetime.now().strftime('%Y%m%d-%H%M%S')}.txt")
_log_file.touch()


def set_verbose(enabled: bool) -> None:
    """Enable or disable verbose logging."""
    global _verbose
    _verbose = enabled


def log_to_file(message: str, level: str = "INF") -> None:
    """Write a log entry to the log file.

    Parameters
    ----------
    message : str
        The message to log.
    level : str
        Log level: INF, WRN, ERR, or VER. Defaults to INF.
    """
    if level not in ("INF", "WRN", "ERR", "VER"):
        level = "INF"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(_log_file, "a") as f:
        f.write(f"[{timestamp}] [{level}] {message.replace(chr(10), ' || ').replace(chr(13), ' || ')}\n")


def write(msg: str, color: str = "") -> None:
    """Writes a message to the console without a newline at the end.
    
    Parameters
    ----------
    message : str
        The message to log.
    color : str
        The foreground color to use for colorized text.  Defaults to none (console default).
    """
    write_internal(msg, False, color, "INF")


def writeln(msg: str, color: str = "") -> None:
    """Writes a message to the console with a newline at the end.

    Parameters
    ----------
    message : str
        The message to log.
    color : str
        The foreground color to use for colorized text.  Defaults to none (console default).
    """
    write_internal(msg, True, color, "INF")


def verbose_writeln(msg: str, color: str = "") -> None:
    """Writes a message only when verbose logging is enabled.

    Parameters
    ----------
    message : str
        The message to log.
    color : str
        The foreground color to use for colorized text.  Defaults to none (console default).
    """
    if _verbose:
        write_internal(msg, True, color, "VER")


def _colorize(msg: str) -> str:
    """Replace [OK], [WARN], [ERROR] with their colorized equivalents.
    
    Parameters
    ----------
    message : str
        The message to log.
    color : str
        The foreground color to use for colorized text.  Defaults to none (console default).
    """
    def replace(m: re.Match) -> str:
        tag = m.group(1)
        return f"[{_COLORS[tag]}{tag}{Style.RESET_ALL}]"
    return _TAG_RE.sub(replace, msg)


def write_internal(msg: str, last: bool = False, color: str = "", level: str = "INF") -> None:
    """Overwrite the current terminal line with msg.  If last=True, end with a newline.

    Parameters
    ----------
    message : str
        The message to log.
    last : bool
        True if this is the last line to log and a newline is required; otherwise false.  Defaults
        to False.
    color : str
        The foreground color to use for colorized text.  Defaults to none (console default).
    level : str
        The logging level for this message.
    """
    terminal_size = shutil.get_terminal_size().columns
    colored_msg = f"{color}{_colorize(msg)}{Style.RESET_ALL}" if color else _colorize(msg)
    print(f"\r{colored_msg:<{terminal_size}}", end="\n" if last else "", flush=True)
    log_to_file(msg, level)

