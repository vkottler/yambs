"""
A module implementing a dependency manager.
"""

# built-in
from enum import StrEnum, auto
from pathlib import Path
from typing import Any, Callable, Dict

# third-party
from vcorelib.io import ARBITER

# internal
from yambs.dependency.config import (
    Dependency,
    DependencyKind,
    DependencySource,
)
from yambs.dependency.github import GithubDependency

DependencyData = Dict[str, Any]


class DependencyState(StrEnum):
    """States that a dependency can be in."""

    INIT = auto()


def yambs_handler(
    root: Path, dep: Dependency, current: DependencyState, data: DependencyData
) -> DependencyState:
    """Handle a yambs dependency."""

    # No other source implementations currently.
    assert dep.source == DependencySource.GITHUB

    # Ensure repository parameters are set.
    assert "owner" in dep.github, dep
    assert "repo" in dep.github, dep

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


DependencyHandler = Callable[
    [Path, Dependency, DependencyState, DependencyData], DependencyState
]

HANDLERS: Dict[DependencyKind, DependencyHandler] = {
    DependencyKind.YAMBS: yambs_handler
}


class DependencyManager:
    """A class for managing project dependencies."""

    def __init__(self, root: Path) -> None:
        """Initialize this instance."""

        self.root = root
        self.state_path = self.root.joinpath("state.json")
        self.state = ARBITER.decode(self.state_path).data

    def save(self) -> None:
        """Save state data."""

        ARBITER.encode(self.state_path, self.state)

    def audit(self, dep: Dependency) -> DependencyState:
        """Interact with a dependency if needed."""

        dep_data: DependencyData = self.state.setdefault(
            str(dep),
            {},
        )  # type: ignore

        state = HANDLERS[dep.kind](
            self.root,
            dep,
            DependencyState(dep_data.setdefault("state", "init")),
            dep_data.setdefault("handler", {}),
        )

        # Update state.
        dep_data["state"] = str(state.value)

        return state
