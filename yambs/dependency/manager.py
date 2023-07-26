"""
A module implementing a dependency manager.
"""

# built-in
from pathlib import Path

# third-party
from vcorelib.io import ARBITER

# internal
from yambs.dependency.config import Dependency, DependencyData
from yambs.dependency.handlers import HANDLERS
from yambs.dependency.state import DependencyState


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
