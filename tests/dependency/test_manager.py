"""
Test the 'dependency.manager' module.
"""

# module under test
from yambs.dependency.manager import DependencyManager


def test_dependency_manager_basic():
    """Test basic interactions with a dependency manager."""

    assert DependencyManager()
