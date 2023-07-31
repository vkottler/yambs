"""
Test the 'dependency.manager' module.
"""

# built-in
from pathlib import Path
from tempfile import TemporaryDirectory

# module under test
from yambs.dependency.manager import DependencyManager


def test_dependency_manager_basic():
    """Test basic interactions with a dependency manager."""

    with TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        assert DependencyManager(tmp_path, tmp_path)
