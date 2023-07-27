"""
A module declaring shared types.
"""

# built-in
from pathlib import Path
from typing import Callable, List, NamedTuple

# internal
from yambs.dependency.config import Dependency, DependencyData
from yambs.dependency.state import DependencyState


class DependencyTask(NamedTuple):
    """A container for dependency handler invocation data."""

    # Useful paths.
    root: Path
    include: Path
    static: Path

    build_commands: List[List[str]]

    compile_flags: List[str]
    link_flags: List[str]

    dep: Dependency
    current: DependencyState
    data: DependencyData


DependencyHandler = Callable[[DependencyTask], DependencyState]
