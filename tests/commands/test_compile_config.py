"""
Test the 'commands.compile_config' module.
"""

# internal
from tests.resources import resource

# module under test
from yambs import PKG_NAME
from yambs.entry import main as yambs_main


def test_compile_config_command_basic():
    """Test the 'compile_config' command."""

    base = [
        PKG_NAME,
        "compile_config",
        str(resource("compile_config_out.json")),
    ]

    in1 = str(resource("compile_config_in1.yaml"))

    assert yambs_main(base + [in1]) == 0
    assert yambs_main(base + ["-e", in1]) == 0
    assert yambs_main(base + ["-e", "-u", in1]) == 0
    assert yambs_main(base + ["-u", in1]) == 0
