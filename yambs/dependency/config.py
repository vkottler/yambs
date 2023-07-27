"""
A module for working with dependency configurations.
"""

# built-in
from enum import StrEnum, auto
from typing import Any, Dict, Optional, cast

# third-party
from vcorelib.dict.codec import BasicDictCodec as _BasicDictCodec
from vcorelib.io import JsonObject as _JsonObject

# internal
from yambs.schemas import YambsDictCodec as _YambsDictCodec


class DependencyKind(StrEnum):
    """All dependency kind options."""

    YAMBS = auto()


class DependencySource(StrEnum):
    """All dependency source options."""

    GITHUB = auto()


DependencyData = Dict[str, Any]


class Dependency(_YambsDictCodec, _BasicDictCodec):
    """A class for describing project dependencies."""

    def __str__(self) -> str:
        """Get this dependency as a string."""

        # Change this when other sources are supported.
        assert self.source == DependencySource.GITHUB
        return f"{self.github['owner']}-{self.github['repo']}"

    def __hash__(self) -> int:
        """Compute a hash for this dependency."""
        return hash(str(self))

    def init(self, data: _JsonObject) -> None:
        """Initialize this instance."""

        self.kind = DependencyKind(cast(str, data["kind"]))
        self.source = DependencySource(cast(str, data["source"]))
        self.github: Dict[str, Optional[str]] = data.get(
            "github",
            {},  # type: ignore
        )
        self.target: str = data["target"]  # type: ignore
