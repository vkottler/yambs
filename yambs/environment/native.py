"""
A module implementing a native-build environment.
"""

# built-in
from pathlib import Path
from typing import Set

# third-party
from vcorelib import DEFAULT_ENCODING
from vcorelib.logging import LoggerMixin

# internal
from yambs.aggregation import collect_files, populate_sources
from yambs.config.native import Native
from yambs.generate.common import get_jinja
from yambs.generate.variants import generate as generate_variants


class NativeBuildEnvironment(LoggerMixin):
    """A class implementing a native-build environment."""

    def __init__(self, config: Native) -> None:
        """Initialize this instance."""

        super().__init__()

        self.config = config

        # Collect sources.
        self.sources = collect_files(config.src_root)
        self.apps: Set[Path] = set()
        self.regular: Set[Path] = set()
        populate_sources(
            self.sources, config.src_root, self.apps, self.regular
        )

    def generate(self) -> None:
        """Generate ninja files."""

        with self.config.root.joinpath("build.ninja").open(
            "w", encoding=DEFAULT_ENCODING
        ) as path_fd:
            print(path_fd)

        jinja = get_jinja()
        generate_variants(jinja, self.config)
