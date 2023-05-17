"""
Test the 'commands.uf2conv' module.
"""

# third-party
from vcorelib.paths.context import tempfile

# internal
from tests.resources import resource

# module under test
from yambs import PKG_NAME
from yambs.entry import main as yambs_main


def test_uf2conv_basic():
    """Test the 'uf2conv' command."""

    base = [PKG_NAME, "uf2conv", "-c"]

    assert yambs_main(base) != 0

    assert yambs_main(base + ["-l"]) == 0

    with tempfile() as tmp:
        for kind in ["bin", "hex"]:
            output = ["-o", str(tmp)]
            args = output + [str(resource(f"test1.{kind}"))]
            assert yambs_main(base + args) == 0
            assert yambs_main(base + ["--carray"] + args) == 0
            assert yambs_main(base + ["--info"] + args) == 0
            assert yambs_main(base + ["-f", "0x16573617"] + args) == 0
            assert yambs_main(base + ["-f", "SAML21"] + args) == 0
            assert yambs_main(base + ["-f", "bad"] + args) != 0

        assert (
            yambs_main(
                base + output + [str(resource("pi_pico_circuitpython.uf2"))]
            )
            == 0
        )
        assert (
            yambs_main(
                base
                + output
                + ["--carray", str(resource("pi_pico_circuitpython.uf2"))]
            )
            == 0
        )
        assert (
            yambs_main(
                base
                + output
                + ["--info", str(resource("pi_pico_circuitpython.uf2"))]
            )
            == 0
        )
        assert (
            yambs_main(
                base
                + output
                + ["--info", str(resource("pi_pico_circuitpython.uf2"))]
            )
            == 0
        )
