"""
An entry-point for the 'dist' command.
"""

# built-in
from argparse import ArgumentParser as _ArgumentParser
from argparse import Namespace as _Namespace
from os import linesep
from shutil import make_archive, rmtree

# third-party
from vcorelib import DEFAULT_ENCODING as _DEFAULT_ENCODING
from vcorelib.args import CommandFunction as _CommandFunction
from vcorelib.paths import file_hash_hex
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
    algorithm = "sha256"
    hex_digest = dist.joinpath(f"{slug}.{algorithm}")
    with hex_digest.open("w", encoding=_DEFAULT_ENCODING) as sha_fd:
        for archive in archives:
            sha_fd.write(file_hash_hex(archive, algorithm=algorithm))
            sha_fd.write(" *")
            sha_fd.write(archive.name)
            sha_fd.write(linesep)

    print(f"Wrote '{hex_digest}'.")

    return 0


def add_dist_cmd(parser: _ArgumentParser) -> _CommandFunction:
    """Add dist-command arguments to its parser."""

    add_config_arg(parser)
    return dist_cmd
