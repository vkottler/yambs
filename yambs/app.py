# =====================================
# generator=datazen
# version=3.2.0
# hash=4b61ad6ad675ba2556b5e4af32b9d400
# =====================================

"""
This package's command-line entry-point application.
"""

# built-in
from argparse import ArgumentParser as _ArgumentParser
from argparse import Namespace as _Namespace
from typing import Optional as _Optional

# third-party
from vcorelib.args import CommandFunction as _CommandFunction
from vcorelib.args import app_args as _app_args

# internal
from yambs.commands.all import commands

COMMAND: _Optional[_CommandFunction] = None


def entry(args: _Namespace) -> int:
    """Execute the requested task."""

    assert COMMAND is not None
    return COMMAND(args)


def add_app_args(parser: _ArgumentParser) -> None:
    """Add application-specific arguments to the command-line parser."""
    global COMMAND  # pylint: disable=global-statement
    add, COMMAND = _app_args(commands, {})
    add(parser)
