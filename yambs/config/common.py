"""
A module for common configuration interfaces.
"""

# built-in
from pathlib import Path
from typing import Any, Dict, Type, TypeVar

# third-party
from vcorelib.dict import merge
from vcorelib.dict.codec import BasicDictCodec as _BasicDictCodec
from vcorelib.io import ARBITER as _ARBITER
from vcorelib.io import DEFAULT_INCLUDES_KEY
from vcorelib.io.types import JsonObject as _JsonObject
from vcorelib.paths import Pathlike, find_file, normalize

# internal
from yambs import PKG_NAME

T = TypeVar("T", bound="CommonConfig")
DEFAULT_CONFIG = f"{PKG_NAME}.yaml"


class CommonConfig(_BasicDictCodec):
    """A common, base configuration."""

    data: Dict[str, Any]

    root: Path
    src_root: Path
    build_root: Path
    ninja_root: Path

    def directory(self, name: str, mkdir: bool = True) -> Path:
        """Get a configurable directory."""

        name_root = Path(str(self.data[name]))
        if not name_root.is_absolute():
            name_root = self.root.joinpath(name_root)

        if mkdir:
            name_root.mkdir(parents=True, exist_ok=True)

        return name_root

    def init(self, data: _JsonObject) -> None:
        """Initialize this instance."""

        self.data = data
        self.root = Path()

        self.src_root = self.directory("src_root")
        self.build_root = self.directory("build_root")
        self.ninja_root = self.directory("ninja_out")

    @classmethod
    def load(
        cls: Type[T],
        path: Pathlike = DEFAULT_CONFIG,
        package_config: str = DEFAULT_CONFIG,
        root: Pathlike = None,
    ) -> T:
        """Load a configuration."""

        src_config = find_file(package_config, package=PKG_NAME)
        assert src_config is not None

        data = merge(
            _ARBITER.decode(
                src_config,
                includes_key=DEFAULT_INCLUDES_KEY,
                require_success=True,
            ).data,
            _ARBITER.decode(path, includes_key=DEFAULT_INCLUDES_KEY).data,
            # Always allow the project-specific configuration to override
            # package data.
            expect_overwrite=True,
        )

        result = cls.create(data)

        if root is not None:
            result.root = normalize(root)
            result.root.mkdir(parents=True, exist_ok=True)

        return result
