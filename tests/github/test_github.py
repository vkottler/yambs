"""
Test the 'github' module.
"""

# internal
from tests.resources import OWNER, REPO

# module under test
from yambs.github import (
    github_url,
    latest_release_data,
    latest_repo_release_api_url,
)


def test_github_url_basic():
    """Test URL encoding."""

    assert github_url().geturl() == "https://github.com"
    assert github_url(netloc_prefix="api").geturl() == "https://api.github.com"
    assert (
        latest_repo_release_api_url(OWNER, REPO)
        == "https://api.github.com/repos/vkottler/yambs-sample/releases/latest"
    )
    assert latest_release_data(OWNER, REPO)
