"""
Common command-line argument interfaces.
"""

# built-in
from argparse import ArgumentParser as _ArgumentParser
from pathlib import Path as _Path

# internal
from yambs.config.common import DEFAULT_CONFIG


def add_common_args(parser: _ArgumentParser) -> None:
    """Add common command-line arguments to a parser."""

    parser.add_argument(
        "-c",
        "--config",
        type=_Path,
        default=DEFAULT_CONFIG,
        help=(
            "the path to the top-level configuration "
            "file (default: '%(default)s')"
        ),
    )
    parser.add_argument(
        "-i",
        "--single-pass",
        action="store_true",
        help="only run a single watch iteration",
    )
    parser.add_argument(
        "-w",
        "--watch",
        action="store_true",
        help="whether or not to continue watching for source tree changes",
    )
