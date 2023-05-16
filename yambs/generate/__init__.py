"""
A module for generating templated outputs.
"""

# built-in
from os import linesep
from pathlib import Path
from typing import Any, Dict

# third-party
from datazen.templates import environment
from jinja2 import Environment, FileSystemLoader
from vcorelib import DEFAULT_ENCODING
from vcorelib.paths import resource

# internal
from yambs import PKG_NAME
from yambs.config import Config


def render_template(
    jinja: Environment, root: Path, name: str, data: Dict[str, Any]
) -> None:
    """Render a single template."""

    with root.joinpath(name).open("w", encoding=DEFAULT_ENCODING) as path_fd:
        path_fd.write(jinja.get_template(f"{name}.j2").render(data))
        path_fd.write(linesep)


def generate(root: Path, config: Config) -> None:
    """Generate ninja files."""

    templates_dir = resource("templates", package=PKG_NAME)
    assert templates_dir is not None

    jinja = environment(
        loader=FileSystemLoader([templates_dir], followlinks=True)
    )

    root.mkdir(parents=True, exist_ok=True)

    # Render the top-level configuration. This is the only file that's
    # generated into the root directory.
    render_template(jinja, root, "build.ninja", config.data)

    ninja_root = Path(str(config.data["ninja_out"]))
    if not ninja_root.is_absolute():
        ninja_root = root.joinpath(ninja_root)
    ninja_root.mkdir(parents=True, exist_ok=True)

    # Render the board manifest.
    render_template(jinja, ninja_root, "all.ninja", config.data)
