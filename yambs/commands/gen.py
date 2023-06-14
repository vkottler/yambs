"""
An entry-point for the 'gen' command.
"""

# built-in
from argparse import ArgumentParser as _ArgumentParser
from argparse import Namespace as _Namespace
from pathlib import Path as _Path
from sys import executable

# third-party
from rcmpy.watch import watch
from rcmpy.watch.params import WatchParams
from vcorelib.args import CommandFunction as _CommandFunction

# internal
from yambs import PKG_NAME
from yambs.commands.common import add_common_args
from yambs.config import Config
from yambs.environment import BuildEnvironment
from yambs.generate import generate


def gen_cmd(args: _Namespace) -> int:
    """Execute the gen command."""

    env = BuildEnvironment(Config.load(path=args.config, root=args.dir))
    generate(env)

    return (
        watch(
            WatchParams(
                args.dir,
                _Path(str(env.config.data["src_root"])),
                [
                    executable,
                    "-m",
                    PKG_NAME,
                    "-C",
                    str(args.dir),
                    "gen",
                    "-c",
                    str(args.config),
                ],
                False,  # Don't check file contents.
                single_pass=args.single_pass,
            )
        )
        if args.watch
        else 0
    )


def add_gen_cmd(parser: _ArgumentParser) -> _CommandFunction:
    """Add gen-command arguments to its parser."""

    add_common_args(parser)
    return gen_cmd
