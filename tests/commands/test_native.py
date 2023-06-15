"""
Test the 'commands.native' module.
"""

# internal
from tests.resources import resource

# module under test
from yambs import PKG_NAME
from yambs.entry import main as yambs_main


def test_native_command_basic():
    """Test the 'native' command."""

    assert (
        yambs_main(
            [
                PKG_NAME,
                "-C",
                str(resource("scenarios", "native")),
                "native",
                "-w",
                "-i",
            ]
        )
        == 0
    )
