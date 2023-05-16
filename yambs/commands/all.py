# =====================================
# generator=datazen
# version=3.1.2
# hash=cb9e0150c875bbd5c9a734e5c037a6bd
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
from yambs.commands.gen import add_gen_cmd


def commands() -> _List[_Tuple[str, str, _CommandRegister]]:
    """Get this package's commands."""

    return [
        (
            "gen",
            "poll the source tree and generate any new build files",
            add_gen_cmd,
        ),
        ("noop", "command stub (does nothing)", lambda _: lambda _: 0),
    ]
