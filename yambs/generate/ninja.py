"""
A module for working with ninja syntax.
"""

# built-in
from os import linesep
from pathlib import Path
from typing import Set, TextIO


def write_source_line(
    stream: TextIO,
    source: Path,
    base: Path,
    current_sources: Set[Path],
    board: str = None,
) -> Path:
    """Write a ninja configuration line for a source file."""

    dest = source
    if board is not None:
        dest = source.parent.joinpath(board, source.name)

    # Don't generate any duplicate compilation rules.
    if dest not in current_sources:
        current_sources.add(dest)

        stream.write(
            (
                f"build $build_dir/"
                f"{dest.relative_to(base).with_suffix('.o')}: "
                f"cc $src_dir/{source.relative_to(base)}"
            )
            + linesep
        )

    return dest


def write_continuation(stream: TextIO, offset: str) -> None:
    """Write a line continuation."""
    stream.write(" $" + linesep + offset)


def write_link_line(
    stream: TextIO, source: Path, all_srcs: Set[Path], base: Path
) -> None:
    """
    Write a ninja configuration line for an application requiring linking.
    """

    source = source.relative_to(base)

    elf = f"$build_dir/{source.with_suffix('.elf')}"
    line = f"build {elf}: link "
    offset = " " * len(line)
    stream.write(line + f"$build_dir/{source.with_suffix('.o')}")

    for src in all_srcs:
        write_continuation(stream, offset)
        stream.write(f"$build_dir/{src.relative_to(base).with_suffix('.o')}")
    stream.write(linesep)

    # Add lines for creating binaries.
    bin_path = f"$build_dir/{source.with_suffix('.bin')}"
    stream.write(f"build {bin_path}: bin {elf}" + linesep)

    # Add an hex target.
    hex_path = f"$build_dir/{source.with_suffix('.hex')}"
    stream.write(f"build {hex_path}: hex {elf}" + linesep)

    # Add an objdump target.
    dump_path = f"$build_dir/{source.with_suffix('.dump')}"
    stream.write(f"build {dump_path}: dump {elf}" + linesep)

    # Add a uf2 target.
    uf2_path = f"$build_dir/{source.with_suffix('.uf2')}"
    stream.write(f"build {uf2_path}: uf2 {hex_path}" + linesep + linesep)


def write_phony(
    stream: TextIO, app_srcs: Set[Path], base: Path, board: str
) -> None:
    """Write the phony target."""

    phonies = [
        ("apps", ".bin"),
        ("hexs", ".hex"),
        ("dumps", ".dump"),
        ("uf2s", ".uf2"),
    ]

    if app_srcs:
        for phony, suffix in phonies:
            srcs = list(app_srcs)
            first = srcs[0].relative_to(base)
            srcs = srcs[1:]

            line = f"build {board}_{phony}: phony "
            offset = " " * len(line)
            stream.write(line + f"$build_dir/{first.with_suffix(suffix)}")
            for src in srcs:
                write_continuation(stream, offset)
                src = src.relative_to(base)
                stream.write(f"$build_dir/{src.with_suffix(suffix)}")

            stream.write(linesep)
