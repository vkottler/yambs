"""
An entry-point for the 'native' command.
"""

# built-in
from argparse import ArgumentParser as _ArgumentParser
from argparse import Namespace as _Namespace

from vcorelib import DEFAULT_ENCODING

# third-party
from vcorelib.args import CommandFunction as _CommandFunction

# internal
from yambs.commands.common import add_common_args
from yambs.config.native import Native

DEFAULT_TARGET = "debug"


def native_cmd(args: _Namespace) -> int:
    """Execute the native command."""

    config = Native.load(
        path=args.config, root=args.dir, package_config="native.yaml"
    )

    # src/apps              - all sources are applications to link
    # collect src/apps sources

    # src/* (except 'apps') - sources to link executables with
    # collect all other sources

    with config.root.joinpath("build.ninja").open(
        "w", encoding=DEFAULT_ENCODING
    ) as path_fd:
        print(path_fd)

    # generate recipes? or use jinja template

    for variant, data in config.data["variants"].items():
        # generate rules for all variants
        build = config.build_root.joinpath(variant)
        build.mkdir(exist_ok=True, parents=True)
        print(data)

    return 0


def add_native_cmd(parser: _ArgumentParser) -> _CommandFunction:
    """Add native-command arguments to its parser."""

    add_common_args(parser)
    return native_cmd
