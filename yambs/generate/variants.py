"""
A module for generating variant-related files.
"""

# built-in
from contextlib import contextmanager
from typing import Any, Dict, Iterator, List

# third-party
from jinja2 import Environment

# internal
from yambs.config.common import CommonConfig
from yambs.generate.common import render_template


@contextmanager
def modified_variant_data(
    name: str, data: Dict[str, Any], cflag_groups: Dict[str, List[str]]
) -> Iterator[None]:
    """
    Ensure that cflag groups are processed, and that the variant has access to
    its name while rendering.
    """

    orig = []
    if "extra_cflags" in data:
        orig = data["extra_cflags"]

        # Process cflag groups.
        flags = set(orig + cflag_groups.get(name, []))
        for group in data["cflag_groups"]:
            flags |= set(cflag_groups[group])

        data["extra_cflags"] = flags

    data["name"] = name

    yield

    del data["name"]
    if "extra_cflags" in data:
        data["extra_cflags"] = orig


def generate(
    jinja: Environment,
    config: CommonConfig,
    cflag_groups: Dict[str, List[str]],
) -> None:
    """Generate variant-related ninja files."""

    for name, data in config.data["variants"].items():
        variants_root = config.ninja_root.joinpath("variants", name)
        variants_root.mkdir(parents=True, exist_ok=True)
        with modified_variant_data(name, data, cflag_groups):
            render_template(
                jinja,
                variants_root,
                "variant.ninja",
                data,
            )
