"""
A module for writing formatting-related ninja build rules.
"""

# built-in
from os import linesep
from pathlib import Path
from typing import Iterable, TextIO

# third-party
from vcorelib import DEFAULT_ENCODING

# internal
from yambs.config.common import CommonConfig
from yambs.generate.ninja import write_continuation


def render_format(config: CommonConfig, paths: Iterable[Path]) -> None:
    """Render the ninja source for formatting files."""

    with config.ninja_root.joinpath("format.ninja").open(
        "w", encoding=DEFAULT_ENCODING
    ) as path_fd:
        write_format_target(path_fd, paths)


def write_format_target(stream: TextIO, paths: Iterable[Path]) -> None:
    """
    Write rules and targets for running clang-format on first-party sources
    and headers.
    """

    # Actually formats sources.
    stream.write("rule clang-format" + linesep)
    stream.write("  command = clang-format -i $in" + linesep + linesep)

    # Just checks formatting.
    stream.write("rule clang-format-check" + linesep)
    stream.write("  command = clang-format -n --Werror $in" + linesep)

    paths = list(paths)
    if paths:
        for suffix in ["", "-check"]:
            stream.write(linesep)
            line = f"build format{suffix}: clang-format{suffix} "
            offset = " " * len(line)

            stream.write(line)
            stream.write(str(paths[0]))

            for source in paths[1:]:
                write_continuation(stream, offset)
                stream.write(str(source))

            stream.write(linesep)
