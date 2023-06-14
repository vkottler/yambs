"""
An entry-point for the 'native' command.
"""

# built-in
from argparse import ArgumentParser as _ArgumentParser
from argparse import Namespace as _Namespace

# third-party
from vcorelib.args import CommandFunction as _CommandFunction

# internal
from yambs.commands.common import add_common_args

DEFAULT_TARGET = "debug"


def native_cmd(args: _Namespace) -> int:
    """Execute the native command."""

    # Build the 'debug' variant by default.
    if not args.variants:
        args.variants.append(DEFAULT_TARGET)

    # src/apps              - all sources are applications to link
    # src/* (except 'apps') - sources to link executables with

    # configurable build variants, defaults are 'debug' and 'optimized'

    # built outputs go under build/<variant>

    # generate a single build.ninja with everything in it? (at least to start)

    print(args)

    return 0


def add_native_cmd(parser: _ArgumentParser) -> _CommandFunction:
    """Add native-command arguments to its parser."""

    add_common_args(parser)
    parser.add_argument(
        "variants",
        nargs="*",
        help=(
            "variants to build (defaults to "
            f"'{DEFAULT_TARGET}' if not specified)"
        ),
    )

    return native_cmd
