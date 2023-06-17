"""
A module implementing a native-build environment.
"""

# built-in
from os import linesep
from pathlib import Path
from typing import List, Set, TextIO

# third-party
from vcorelib.logging import LoggerMixin

# internal
from yambs.aggregation import collect_files, populate_sources, sources_headers
from yambs.config.native import Native
from yambs.generate.common import get_jinja, render_template
from yambs.generate.ninja import write_continuation
from yambs.generate.ninja.format import render_format
from yambs.generate.variants import generate as generate_variants
from yambs.translation import get_translator


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
        self.logger.info("Rendered '%s'.", root.joinpath(name))

    def write_compile_line(self, stream: TextIO, path: Path) -> Path:
        """Write a single source-compile line."""

        translator = get_translator(path)
        from_src = path.relative_to(self.config.src_root)

        out = translator.output(from_src)

        stream.write(f"build {out}: {translator.rule} $src_dir/{from_src}")
        stream.write(linesep)

        return out

    def write_source_rules(self, stream: TextIO) -> Set[Path]:
        """Write source rules."""
        return {self.write_compile_line(stream, path) for path in self.regular}

    def write_app_rules(
        self, stream: TextIO, outputs: Set[Path]
    ) -> List[Path]:
        """Write app rules."""

        elfs: List[Path] = []

        for path in self.apps:
            out = self.write_compile_line(stream, path)

            from_src = path.relative_to(self.config.src_root)
            elf = Path("$build_dir", from_src.with_suffix(".elf"))
            elfs.append(elf)
            line = f"build {elf}: link "
            offset = " " * len(line)

            stream.write(line + str(out))

            for file in outputs:
                write_continuation(stream, offset)
                stream.write(str(file))

            stream.write(linesep + linesep)

        line = "build ${variant}_apps: phony "
        offset = " " * len(line)

        stream.write(line + str(elfs[0]))
        for elf in elfs[1:]:
            write_continuation(stream, offset)
            stream.write(str(elf))
        stream.write(linesep)

        return elfs

    def generate(self, sources_only: bool = False) -> None:
        """Generate ninja files."""

        if not sources_only:
            # Render templates.
            generate_variants(self.jinja, self.config)
            self.render(self.config.root, "build.ninja")
            for template in ["all", "rules"]:
                self.render(self.config.ninja_root, f"{template}.ninja")

        # Render sources file.
        path = self.config.ninja_root.joinpath("sources.ninja")
        with path.open("w") as path_fd:
            outputs = self.write_source_rules(path_fd)
            self.logger.info("Wrote '%s'.", path)

        # Render apps file.
        path = self.config.ninja_root.joinpath("apps.ninja")
        with path.open("w") as path_fd:
            self.write_app_rules(path_fd, outputs)
            self.logger.info("Wrote '%s'.", path)

        # Render format file.
        render_format(self.config, sources_headers(self.sources))
