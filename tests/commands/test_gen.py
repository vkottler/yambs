"""
Test the 'commands.gen' module.
"""

# internal
from tests.resources import clean_scenario

# module under test
from yambs import PKG_NAME
from yambs.entry import main as yambs_main


def test_gen_command_basic():
    """Test the 'gen' command."""

    assert (
        yambs_main(
            [
                PKG_NAME,
                "-C",
                str(clean_scenario("sample")),
                "gen",
                "-w",
                "-i",
            ]
        )
        == 0
    )

    assert (
        yambs_main([PKG_NAME, "-C", str(clean_scenario("sample")), "gen"]) == 0
    )
