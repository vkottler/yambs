"""
A module for generating variant-related files.
"""

# third-party
from jinja2 import Environment

# internal
from yambs.config.common import CommonConfig
from yambs.generate.common import render_template


def generate(jinja: Environment, config: CommonConfig) -> None:
    """Generate variant-related ninja files."""

    for name, data in config.data["variants"].items():
        variants_root = config.ninja_root.joinpath("variants", name)
        variants_root.mkdir(parents=True, exist_ok=True)

        data["name"] = name
        render_template(
            jinja,
            variants_root,
            "variant.ninja",
            data,
        )
        del data["name"]
