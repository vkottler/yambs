"""
A module implementing a dependency handler for other yambs projects.
"""

# built-in
from pathlib import Path
from typing import Set

# third-party
import requests
from vcorelib.io.archive import extractall
from vcorelib.paths import Pathlike, normalize, rel, validate_hex_digest

# internal
from yambs.config.common import DEFAULT_CONFIG
from yambs.config.native import load_native
from yambs.dependency.config import (
    Dependency,
    DependencyData,
    DependencySource,
)
from yambs.dependency.github import GithubDependency
from yambs.dependency.handlers.types import DependencyTask
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


def audit_extract(root: Path, data: DependencyData) -> Path:
    """
    Ensure the release is extracted (and the archive contents are verified).
    """

    if "directory" not in data:
        # The expected directory is just the name of the tarball with no
        # suffix.
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


def check_nested_dependencies(
    config: DependencyData, nested: Set[Dependency]
) -> None:
    """
    Determine if a dependency's configuration specifies additional
    dependencies. Add them to the provided set if so.
    """

    for dep in config.get("dependencies", []):
        nested.add(Dependency.create(dep))


def audit_config_load(
    root: Path,
    include: Path,
    static: Path,
    data: DependencyData,
    config_path: Pathlike = DEFAULT_CONFIG,
) -> DependencyData:
    """
    Load a dependency's configuration data (from disk if necessary) and
    return the result.
    """

    if "dependencies" not in data:
        config_path = normalize(config_path)
        path = config_path
        if not path.is_absolute():
            path = root.joinpath(path)

        assert path.is_file(), path

        config = load_native(path=path, root=root)

        # Ensure some directory linkages are set up ('static' and 'include').
        config.third_party_root.mkdir(parents=True, exist_ok=True)

        for source in [include, static]:
            dest = config.third_party_root.joinpath(source.name)
            if not dest.is_symlink():
                dest.symlink_to(source)

        # It's not necessary to keep track of the entire configuration.
        data["dependencies"] = [x.asdict() for x in config.dependencies]

    return data


def yambs_handler(task: DependencyTask) -> DependencyState:
    """Handle a yambs dependency."""

    # No other source implementations currently.
    assert task.dep.source == DependencySource.GITHUB

    github = github_release(task.dep, task.data)
    audit_downloads(task.root, task.data, github)
    directory = audit_extract(task.root, task.data)

    static_lib = directory.joinpath(
        "build", task.dep.target, f"{task.data['slug']}.a"
    )
    task.data["static_library"] = str(static_lib)

    if not static_lib.is_file():
        # Add a build command if the library still needs to be built.
        task.build_commands.append(
            ["ninja", "-C", str(rel(directory)), f"{task.dep.target}_lib"]
        )

    # Ensure the final static library is linked within the static directory.
    static_include = task.static.joinpath(f"lib{static_lib.name}")
    if not static_include.is_symlink():
        static_include.symlink_to(
            Path("..", static_lib.relative_to(task.root))
        )

    # Ensure this dependency's static library gets linked.
    task.link_flags.append(f"-l{task.data['slug']}")

    # Ensure the 'src' directory is linked within the include directory.
    src_include = task.include.joinpath(task.data["name"])
    if not src_include.is_symlink():
        src_include.symlink_to(Path("..", task.data["name"], "src"))

    # Check if loading the project configuration data is necessary.
    # Read the project's configuration data to find any nested dependencies.
    check_nested_dependencies(
        audit_config_load(directory, task.include, task.static, task.data),
        task.nested,
    )

    return task.current
