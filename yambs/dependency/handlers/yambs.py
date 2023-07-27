"""
A module implementing a dependency handler for other yambs projects.
"""

# built-in
from pathlib import Path

# third-party
import requests
from vcorelib.io.archive import extractall
from vcorelib.paths import validate_hex_digest

# internal
from yambs.dependency.config import (
    Dependency,
    DependencyData,
    DependencySource,
)
from yambs.dependency.github import GithubDependency
from yambs.dependency.state import DependencyState

TARBALL = ".tar.xz"


def audit_downloads(
    root: Path, data: DependencyData, github: GithubDependency
) -> None:
    """Ensure release assets are downloaded."""

    to_download = ["sum", TARBALL]
    for asset in github.data["assets"]:
        name = asset["name"]

        dest = root.joinpath(name)

        if dest.is_file():
            continue

        for suffix in to_download:
            if name.endswith(suffix):
                # Download the file.
                req = requests.get(asset["browser_download_url"], timeout=10)
                with dest.open("wb") as dest_fd:
                    for chunk in req.iter_content(chunk_size=4096):
                        dest_fd.write(chunk)

                data["assets"][suffix] = str(dest)
                break


def github_release(dep: Dependency, data: DependencyData) -> GithubDependency:
    """Obtain GitHub release metadata from the project if necessary."""

    # Ensure repository parameters are set.
    assert "owner" in dep.github and dep.github["owner"], dep
    assert "repo" in dep.github and dep.github["repo"], dep

    # Load GitHub release data.
    github = GithubDependency(
        dep.github["owner"],
        dep.github["repo"],
        data=data.get("latest_release"),
    )

    # Initialize data.
    data["latest_release"] = github.data
    data["version"] = github.data["tag_name"]
    data.setdefault("assets", {})

    return github


def audit_extract(root: Path, data: DependencyData) -> str:
    """
    Ensure the release is extracted (and the archive contents are verified).
    """

    if "directory" not in data:
        # The expected directory is just the name of the tarball with no
        # suffix.
        expected = Path(data["assets"][TARBALL].replace(TARBALL, ""))

        # The name of the project is the directory name without the version
        # suffix.
        data["name"] = expected.name.replace(f"-{data['version']}", "")

        # check if need to un-archive, if so, verify checksum.
        if not expected.is_dir():
            validate_hex_digest(data["assets"]["sum"], root=root)
            assert extractall(
                data["assets"][TARBALL],
                dst=root,
                maxsplit=1 + expected.name.count("."),
            )[0]
            assert expected.is_dir()

        data["directory"] = str(expected)

    assert "name" in data
    return data["directory"]  # type: ignore


def yambs_handler(
    root: Path, dep: Dependency, current: DependencyState, data: DependencyData
) -> DependencyState:
    """Handle a yambs dependency."""

    # No other source implementations currently.
    assert dep.source == DependencySource.GITHUB

    github = github_release(dep, data)
    audit_downloads(root, data, github)
    directory = Path(audit_extract(root, data))
    print(directory)

    print(current)
    return current
