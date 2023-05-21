"""
A module implementing a configuration interface for the package.
"""

# built-in
from pathlib import Path
from typing import Any, Dict, Iterator, Tuple

# third-party
from vcorelib.dict import merge
from vcorelib.dict.codec import BasicDictCodec as _BasicDictCodec
from vcorelib.io import ARBITER as _ARBITER
from vcorelib.io.types import JsonObject as _JsonObject
from vcorelib.paths import Pathlike, find_file

# internal
from yambs import PKG_NAME
from yambs.config.board import Board
from yambs.schemas import YambsDictCodec as _YambsDictCodec


class Config(_YambsDictCodec, _BasicDictCodec):
    """The top-level configuration object for the package."""

    data: Dict[str, Any]

    def init(self, data: _JsonObject) -> None:
        """Initialize this instance."""

        self.data = data
        self.root = Path()

    def directory(self, name: str, mkdir: bool = True) -> Path:
        """Get a configurable directory."""

        name_root = Path(str(self.data[name]))
        if not name_root.is_absolute():
            name_root = self.root.joinpath(name_root)

        if mkdir:
            name_root.mkdir(parents=True, exist_ok=True)

        return name_root

    def boards(self) -> Iterator[Tuple[Board, Dict[str, Any]]]:
        """Iterate over boards."""

        for board in self.data["boards"]:
            yield Board.from_dict(
                board, self.data["architectures"], self.data["chips"]
            ), board


DEFAULT_CONFIG = f"{PKG_NAME}.yaml"


def load(path: Pathlike = DEFAULT_CONFIG) -> Config:
    """Load a configuration."""

    src_config = find_file(DEFAULT_CONFIG, package=PKG_NAME)
    assert src_config is not None

    return Config.create(
        merge(
            _ARBITER.decode(
                src_config, includes_key="includes", require_success=True
            ).data,
            _ARBITER.decode(path, includes_key="includes").data,
            # Always allow the project-specific configuration to override
            # package data.
            expect_overwrite=True,
        )
    )
