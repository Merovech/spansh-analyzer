"""
Command-line argument parsing for PySpanshCalc.
"""

import argparse


class AppArgs:
    """Parsed command-line arguments."""

    def __init__(self, input_file: str, verbose: bool, console_interval: int) -> None:
        self.input_file = input_file
        self.verbose = verbose
        self.console_interval = console_interval


def parse_args() -> AppArgs:
    """Parse command-line arguments and return an AppArgs instance."""
    parser = argparse.ArgumentParser(
        description="Parse a Spansh galaxy JSON dump and run all extension processors."
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging."
    )
    parser.add_argument(
        "-i", "--input-file",
        required=True,
        metavar="FILE",
        help="Path to the Spansh galaxy JSON file to process."
    )
    parser.add_argument(
        "-n", "--console-interval",
        type=int,
        default=10000,
        metavar="N",
        help="How often (in systems) to update the processing status. Default: 10000."
    )
    parsed = parser.parse_args()
    return AppArgs(
        input_file=parsed.input_file,
        verbose=parsed.verbose,
        console_interval=parsed.console_interval,
    )
