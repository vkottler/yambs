"""
A module for aggregating dependency handlers.
"""

# built-in
from pathlib import Path
from typing import Callable, Dict

# internal
from yambs.dependency.config import Dependency, DependencyData, DependencyKind
from yambs.dependency.handlers.yambs import yambs_handler
from yambs.dependency.state import DependencyState

DependencyHandler = Callable[
    [Path, Dependency, DependencyState, DependencyData], DependencyState
]

HANDLERS: Dict[DependencyKind, DependencyHandler] = {
    DependencyKind.YAMBS: yambs_handler
}
