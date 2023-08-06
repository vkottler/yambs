"""
Test the 'commands.native' module.
"""

# built-in
from shutil import which
from subprocess import run
from sys import platform

# third-party
from vcorelib.paths.context import in_dir

# internal
from tests.resources import clean_scenario

# module under test
from yambs import PKG_NAME
from yambs.entry import main as yambs_main


def test_native_command_basic():
    """Test the 'native' command."""

    path = str(clean_scenario("native"))

    # Ensure the directory dependency is cleaned as well.
    clean_scenario("native2")

    with in_dir(path):
        assert yambs_main([PKG_NAME, "native", "-w", "-i"]) == 0
        assert yambs_main([PKG_NAME, "native"]) == 0

        # Try to build (if we can).
        # Re-enable this when we fix the third party script.
        if platform == "linux" and which("ninja"):
            run(["ninja", "all", "format-check"], check=True)
