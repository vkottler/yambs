"""
A module for working with GitHub releases.
"""

# built-in
import os
from typing import Any, Dict
from urllib.parse import ParseResult

# third-party
import requests
from vcorelib.dict.codec import BasicDictCodec as _BasicDictCodec

# internal
from yambs.schemas import YambsDictCodec as _YambsDictCodec


class Github(_YambsDictCodec, _BasicDictCodec):
    """GitHub repository information."""


def github_url(
    netloc_prefix: str = "",
    scheme: str = "https",
    path: str = "",
    params: str = "",
    query: str = "",
    fragment: str = "",
) -> ParseResult:
    """See: https://docs.python.org/3/library/urllib.parse.html."""

    netloc = "github.com"
    if netloc_prefix:
        netloc = f"{netloc_prefix}." + netloc

    return ParseResult(
        scheme=scheme,
        netloc=netloc,
        path=path,
        params=params,
        query=query,
        fragment=fragment,
    )


def latest_repo_release_api_url(owner: str, repo: str) -> str:
    """Get a URL string for a repository's latest release."""
    return github_url(
        netloc_prefix="api", path=f"repos/{owner}/{repo}/releases/latest"
    ).geturl()


GIHTUB_HEADERS = {
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}


def check_api_token() -> None:
    """Check for a GitHub API token set via the environment."""

    if "Authorization" not in GIHTUB_HEADERS:
        if "GITHUB_API_TOKEN" in os.environ:
            GIHTUB_HEADERS[
                "Authorization"
            ] = f"Bearer {os.environ['GITHUB_API_TOKEN']}"


ReleaseData = Dict[str, Any]


def latest_release_data(
    owner: str, repo: str, *args, timeout: float = None, **kwargs
) -> ReleaseData:
    """Get latest-release data."""

    check_api_token()

    return requests.get(  # type: ignore
        latest_repo_release_api_url(owner, repo),
        *args,
        timeout=timeout,
        headers=GIHTUB_HEADERS,
        **kwargs,
    ).json()
