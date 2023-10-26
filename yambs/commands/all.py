# =====================================
# generator=datazen
# version=3.1.4
# hash=a579de7276b0c8f219e976ab8cc6a008
# =====================================

"""
A module aggregating package commands.
"""

# built-in
from typing import List as _List
from typing import Tuple as _Tuple

# third-party
from vcorelib.args import CommandRegister as _CommandRegister

# internal
from yambs.commands.compile_config import add_compile_config_cmd
from yambs.commands.dist import add_dist_cmd
from yambs.commands.download import add_download_cmd
from yambs.commands.gen import add_gen_cmd
from yambs.commands.native import add_native_cmd
from yambs.commands.uf2conv import add_uf2conv_cmd


def commands() -> _List[_Tuple[str, str, _CommandRegister]]:
    """Get this package's commands."""

    return [
        (
            "compile_config",
            "load configuration data and write results to a file",
            add_compile_config_cmd,
        ),
        (
            "dist",
            "create a source distribution",
            add_dist_cmd,
        ),
        (
            "download",
            "download GitHub release assets",
            add_download_cmd,
        ),
        (
            "gen",
            "poll the source tree and generate any new build files",
            add_gen_cmd,
        ),
        (
            "native",
            "generate build files for native-only target projects",
            add_native_cmd,
        ),
        (
            "uf2conv",
            "convert to UF2 or flash directly",
            add_uf2conv_cmd,
        ),
        ("noop", "command stub (does nothing)", lambda _: lambda _: 0),
    ]
