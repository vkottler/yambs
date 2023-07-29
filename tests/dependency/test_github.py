"""
Test the 'dependency.github' module.
"""

# internal
from tests.resources import OWNER, REPO

# module under test
from yambs.dependency.github import GithubDependency


def test_github_dependency_basic():
    """Test basic interactions with a GitHub dependency."""

    assert GithubDependency(OWNER, REPO)
