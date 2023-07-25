"""
A module implementing a dependency manager.
"""

# built-in
from pathlib import Path

# internal
from yambs.dependency.config import Dependency


class DependencyManager:
    """A class for managing project dependencies."""

    def __init__(self, root: Path) -> None:
        """Initialize this instance."""

        self.root = root

    def audit(self, dep: Dependency) -> None:
        """Interact with a dependency if needed."""

        print(dep)
