"""
Test the 'commands.download' module.
"""

# built-in
from tempfile import TemporaryDirectory

# module under test
from yambs import PKG_NAME
from yambs.entry import main as yambs_main


def test_download_basic():
    """Test the 'download' command."""

    with TemporaryDirectory() as tmpdir:
        assert yambs_main([PKG_NAME, "-C", str(tmpdir), "download"]) == 0
