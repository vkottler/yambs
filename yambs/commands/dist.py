"""
An entry-point for the 'dist' command.
"""

# built-in
from argparse import ArgumentParser as _ArgumentParser
from argparse import Namespace as _Namespace
from shutil import make_archive, rmtree

# third-party
from vcorelib.args import CommandFunction as _CommandFunction
from vcorelib.paths import create_hex_digest
from vcorelib.paths.context import in_dir

# internal
from yambs.commands.common import add_config_arg
from yambs.config.common import CommonConfig


def dist_cmd(args: _Namespace) -> int:
    """Execute the dist command."""

    config = CommonConfig.load(path=args.config, root=args.dir)

    # Remove and re-create the dist directory.
    dist = config.dist_root
    rmtree(dist, ignore_errors=True)
    dist.mkdir()

    slug = str(config.project)
    src = config.src_root
    archives = []

    for ext, kind in [
        ("tar.gz", "gztar"),
        ("tar.xz", "xztar"),
        ("zip", "zip"),
    ]:
        out = src.joinpath(f"{slug}.{ext}")
        out.unlink(missing_ok=True)

        with in_dir(src):
            make_archive(slug, kind)

        assert out.is_file(), out

        final = dist.joinpath(out.name)
        out.rename(final)
        archives.append(final)

        print(f"Created '{final}'.")

    # Produce a hex digest.
    print(f"Wrote '{create_hex_digest(dist, slug)}'.")

    return 0


def add_dist_cmd(parser: _ArgumentParser) -> _CommandFunction:
    """Add dist-command arguments to its parser."""

    add_config_arg(parser)
    return dist_cmd
