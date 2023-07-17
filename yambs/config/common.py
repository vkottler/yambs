"""
A module for common configuration interfaces.
"""

# built-in
from pathlib import Path
from typing import Any, Dict, NamedTuple, Optional, Type, TypeVar

# third-party
from vcorelib.dict import merge
from vcorelib.dict.codec import BasicDictCodec as _BasicDictCodec
from vcorelib.io import ARBITER as _ARBITER
from vcorelib.io import DEFAULT_INCLUDES_KEY
from vcorelib.io.types import JsonObject as _JsonObject
from vcorelib.paths import Pathlike, find_file, normalize

# internal
from yambs import PKG_NAME
from yambs.schemas import YambsDictCodec as _YambsDictCodec

T = TypeVar("T", bound="CommonConfig")
DEFAULT_CONFIG = f"{PKG_NAME}.yaml"


class Project(NamedTuple):
    """An object for managing project metadata."""

    name: str
    major: int
    minor: int
    patch: int

    # GitHub attributes.
    repo: str
    owner: Optional[str]

    @staticmethod
    def create(data: _JsonObject) -> "Project":
        """Create a project instance from JSON data."""

        ver = data["version"]

        name: str = data["name"]  # type: ignore
        github: Dict[str, str] = data.get("github", {})  # type: ignore
        github.setdefault("repo", name)

        return Project(
            name,
            ver["major"],  # type: ignore
            ver["minor"],  # type: ignore
            ver["patch"],  # type: ignore
            github["repo"],
            github.get("owner"),
        )

    @property
    def version(self) -> str:
        """Get this project's version string."""
        return f"{self.major}.{self.minor}.{self.patch}"

    def __str__(self) -> str:
        """Get this project as a string."""
        return f"{self.name}-{self.version}"


class CommonConfig(_YambsDictCodec, _BasicDictCodec):
    """A common, base configuration."""

    data: Dict[str, Any]

    root: Path
    src_root: Path
    build_root: Path
    ninja_root: Path
    dist_root: Path

    file: Optional[Path]

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
        self.dist_root = self.directory("dist_out")

        self.file = None

        self.project = Project.create(data["project"])  # type: ignore

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

        path = normalize(path)

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

        if path.is_file():
            result.file = path

        if root is not None:
            result.root = normalize(root)
            result.root.mkdir(parents=True, exist_ok=True)

        return result
