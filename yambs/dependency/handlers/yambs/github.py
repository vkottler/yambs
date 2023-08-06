"""
A module with interfaces for working with yambs projects found on GitHub.
"""

# built-in
from pathlib import Path

# third-party
import requests
from vcorelib.io.archive import extractall
from vcorelib.paths import validate_hex_digest

# internal
from yambs.dependency.config import Dependency, DependencyData
from yambs.dependency.github import GithubDependency

TARBALL = ".tar.xz"


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


def audit_downloads(
    root: Path, data: DependencyData, github: GithubDependency
) -> None:
    """Ensure release assets are downloaded."""

    to_download = ["sum", TARBALL]
    for asset in github.data["assets"]:
        name = asset["name"]

        dest = root.joinpath(name)

        for suffix in to_download:
            if name.endswith(suffix):
                # Download if necessary.
                if not dest.is_file():
                    # Download the file.
                    req = requests.get(
                        asset["browser_download_url"], timeout=10
                    )
                    with dest.open("wb") as dest_fd:
                        for chunk in req.iter_content(chunk_size=4096):
                            dest_fd.write(chunk)

                data["assets"][suffix] = str(dest)
                break


def audit_extract(root: Path, data: DependencyData) -> Path:
    """
    Ensure the release is extracted (and the archive contents are verified).
    """

    if "directory" not in data:
        # The expected directory is just the name of the tarball with no
        # suffix.
        assert TARBALL in data["assets"], data["assets"]
        expected = Path(data["assets"][TARBALL].replace(TARBALL, ""))

        # The name of the project is the directory name without the version
        # suffix.
        data["slug"] = expected.name
        data["name"] = data["slug"].replace(f"-{data['version']}", "")

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

    # Link 'name' to the destination directory.
    dest_dir = Path(data["directory"])
    name_link = dest_dir.with_name(data["name"])
    if (
        not name_link.is_symlink()
        or str(name_link.readlink()) != dest_dir.name
    ):
        name_link.unlink(missing_ok=True)
        name_link.symlink_to(dest_dir.name)

    return name_link
