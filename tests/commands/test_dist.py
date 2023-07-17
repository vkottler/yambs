"""
Test the 'commands.dist' module.
"""

# internal
from tests.resources import resource

# module under test
from yambs import PKG_NAME
from yambs.entry import main as yambs_main


def test_dist_command_basic():
    """Test the 'dist' command."""

    for scenario in ["sample", "native"]:
        assert (
            yambs_main(
                [
                    PKG_NAME,
                    "-C",
                    str(resource("scenarios", scenario)),
                    "dist",
                    "-s",
                ]
            )
            == 0
        )

        assert (
            yambs_main(
                [
                    PKG_NAME,
                    "-C",
                    str(resource("scenarios", scenario)),
                    "dist",
                ]
            )
            == 0
        )
