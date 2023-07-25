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
        assert DependencyManager(Path(tmp))
