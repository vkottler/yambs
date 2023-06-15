"""
A module implementing a native-build environment.
"""

# built-in
from pathlib import Path
from typing import Set

# third-party
from vcorelib.logging import LoggerMixin

# internal
from yambs.aggregation import collect_files, populate_sources
from yambs.config.native import Native
from yambs.generate.common import get_jinja, render_template
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

        self.jinja = get_jinja()

    def render(self, root: Path, name: str) -> None:
        """Render a template."""
        render_template(
            self.jinja, root, f"native_{name}", self.config.data, out=name
        )

    def generate(self) -> None:
        """Generate ninja files."""

        # Render templates.
        generate_variants(self.jinja, self.config)
        self.render(self.config.root, "build.ninja")
        for template in ["all", "rules"]:
            self.render(self.config.ninja_root, f"{template}.ninja")

        # Render sources file.

        # Render apps file.

        # Render format file.
