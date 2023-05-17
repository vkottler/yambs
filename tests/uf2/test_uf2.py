"""
Test the 'uf2' module.
"""

# internal
from tests.resources import resource

# module under test
from yambs.uf2 import board_id, to_str


def test_board_id():
    """Test the 'board_id' method."""

    assert board_id(str(resource("."))) is not None
    assert board_id(str(resource(".")), info_file="/test.txt") is None
    assert to_str(b"hello") == "hello"
