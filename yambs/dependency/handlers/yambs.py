"""
A module implementing a dependency handler for other yambs projects.
"""

# built-in
from pathlib import Path

# internal
from yambs.dependency.config import (
    Dependency,
    DependencyData,
    DependencySource,
)
from yambs.dependency.github import GithubDependency
from yambs.dependency.state import DependencyState


def yambs_handler(
    root: Path, dep: Dependency, current: DependencyState, data: DependencyData
) -> DependencyState:
    """Handle a yambs dependency."""

    # No other source implementations currently.
    assert dep.source == DependencySource.GITHUB

    # Ensure repository parameters are set.
    assert "owner" in dep.github and dep.github["owner"], dep
    assert "repo" in dep.github and dep.github["repo"], dep

    # Load GitHub release data.
    github = GithubDependency(
        dep.github["owner"],
        dep.github["repo"],
        data=data.get("latest_release"),
    )
    data["latest_release"] = github.data

    print(root)
    print(current)

    return current
