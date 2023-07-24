"""
A module for working with dependency configurations.
"""

# built-in
from enum import StrEnum, auto
from typing import Dict, Optional, cast

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


class Dependency(_YambsDictCodec, _BasicDictCodec):
    """A class for describing project dependencies."""

    def __hash__(self) -> int:
        """Compute a hash for this dependency."""
        return hash(f"{self.github['owner']}-{self.github['repo']}")

    def init(self, data: _JsonObject) -> None:
        """Initialize this instance."""

        self.kind = DependencyKind(cast(str, data["kind"]))
        self.source = DependencySource(cast(str, data["source"]))
        self.github: Dict[str, Optional[str]] = data.get(
            "github", {}  # type: ignore
        )
