"""
PySpanshCalc — main entry point.

Parses a Spansh galaxy JSON dump using the Elite.SpanshTools .NET library,
then routes every StarSystem through all processors found in ./extensions/.

Any processors whose name starts with an underscore are ignored.

Usage:
    python main.py -i <path_to_galaxy.json> [-v] [-n <interval>]
"""

# System imports
import sys
import os
import time

# Project imports
import deps
import processorLoader
import log
import args as cli
from args import AppArgs
from pathlib import Path

# Bootstrap pythonnet / coreclr
try:
    import pythonnet
    pythonnet.load("coreclr")
except Exception as exc:
    print(f"ERROR: Could not load .NET runtime via pythonnet: {exc}")
    print("Make sure .NET 8+ is installed and 'pip install pythonnet' has been run.")
    sys.exit(1)

import clr  # noqa: E402  (must come after pythonnet.load)

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------
# Load the Elite.SpanshTools assembly from ./lib/
LIB_DIR = Path(__file__).parent / "lib"

if not LIB_DIR.exists():
    print("./lib/ directory not found. Downloading dependencies.")
    deps.download_dependencies()

sys.path.insert(0, str(LIB_DIR))

try:
    clr.AddReference("Elite.SpanshTools")
except Exception as exc:
    log.writeln(f"ERROR: Could not load Elite.SpanshTools.dll from {LIB_DIR}: {exc}")
    log.writeln("Please make sure it exists in the lib directory.")
    sys.exit(1)

from Elite.SpanshTools.Parsers import GalaxyParser  # type: ignore # noqa: E402 (because it's loaded at runtime)

# ---------------------------------------------------------------------------
# Main processing loop
# ---------------------------------------------------------------------------
def process_file(app_args: AppArgs) -> None:
    """
    Processes a JSON file from Spansh dumps and feeds each line into all available
    processors.

    Parameters
    ----------
    app_args : AppArgs
        Parsed command-line arguments.
    """

    log.verbose_writeln(f"Args:", log.Fore.CYAN)
    log.verbose_writeln(f"  input_file      : {app_args.input_file}")
    log.verbose_writeln(f"  verbose         : {app_args.verbose}")
    log.verbose_writeln(f"  console_interval: {app_args.console_interval}\n")

    start = time.monotonic()
    extensions_dir = Path(__file__).parent / "extensions"

    log.writeln("Loading processors...")
    processors = processorLoader.load_processors(extensions_dir)
    if not processors:
        log.writeln("No processors found - nothing to do.")
        return

    log.writeln("")

    parser = GalaxyParser()
    async_enumerable = parser.ParseFileAsync(app_args.input_file)
    enumerator = async_enumerable.GetAsyncEnumerator()
    count = 0
    errors = 0
    log.write("Processing.  Systems Processed: 0")
    try:
        # MoveNextAsync() returns ValueTask<bool>. Calling .Result directly on a
        # ValueTask is only valid if it completed synchronously; for file I/O it
        # may not have. Converting to Task<bool> via .AsTask() is always safe to
        # block on with .Result.
        while enumerator.MoveNextAsync().AsTask().Result:
            system = enumerator.Current
            if system is None:
                continue

            count += 1
            for processor in processors:
                try:
                    processor.ProcessSystem(system)
                except Exception as exc:
                    errors += 1
                    calc_name = Path(processor.__file__).name
                    log.writeln(f"[ERROR] {calc_name} / {system.Name}: {exc}")
            if (count % app_args.console_interval == 0):
                log.write(f"Processing.  Systems Processed: {count}")
    finally:
        enumerator.DisposeAsync().AsTask().GetAwaiter().GetResult()

    elapsed = int(time.monotonic() - start)
    hh, remainder = divmod(elapsed, 3600)
    mm, ss = divmod(remainder, 60)
    elapsed_str = f"{hh:02d}:{mm:02d}:{ss:02d}"

    log.writeln("Done.")
    log.writeln("\nProcess statistics:\n-------------------", log.Fore.CYAN)
    log.writeln(f"  Processed: {count}")
    log.writeln(f"  Errors   : {0 if not errors else errors}")
    log.writeln(f"  Elapsed  : {elapsed_str}\n")
    log.writeln("Results:\n--------", log.Fore.CYAN)
    for processor in processors:
        log.verbose_writeln(f"[{processor.GetName()}]")
        processor.Completed()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
def main() -> None:
    if not os.path.isfile(".warnignore"):
        write_warning()
        
    app_args = cli.parse_args()

    log.set_verbose(app_args.verbose)

    if not os.path.isfile(app_args.input_file):
        log.writeln(f"ERROR: File not found: {app_args.input_file}", log.Fore.RED)
        sys.exit(1)
    
    log.writeln(f"[OK] Input file found at '{app_args.input_file}'")

    if Path(app_args.input_file).suffix.lower() != ".json":
        log.writeln(f"ERROR: Input file '{app_args.input_file}' is not a JSON file.", log.Fore.RED)
        sys.exit(1)

    log.writeln(f"[OK] Input file is a JSON file.")

    process_file(app_args)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def write_warning() -> None:
    log.writeln("---------------------------------------------------------------------------")
    log.writeln("WARNING:", log.Fore.RED)
    log.writeln("This tool executes all .py scripts in the ./extensions/ folder to look for")
    log.writeln("processors, then executes the processors on each line of the Spansh data")
    log.writeln("dump.  It does no sandboxing or code restricting on the scripts.  If you")
    log.writeln("do not trust an extension script, DO NOT run it.")
    log.writeln("")
    log.writeln("You can disable a script by either prefixing it with an underscore or by")
    log.writeln("removing it from the ./extensions/ folder.  In either case, those scripts")
    log.writeln("will not be read or executed by the system, but they will be enumerated")
    log.writeln("when the system looks for processors.")
    log.writeln("")
    log.writeln("To suppress this warning, add an empty file to the location of this tool")
    log.writeln("called .warnignore.")
    log.writeln("---------------------------------------------------------------------------")

if __name__ == "__main__":
    main()
