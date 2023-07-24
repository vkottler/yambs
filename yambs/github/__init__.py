"""
A module for working with GitHub releases.
"""

# built-in
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


def latest_release_data(
    owner: str, repo: str, *args, timeout: float = None, **kwargs
) -> Dict[str, Any]:
    """Get latest-release data."""

    return requests.get(  # type: ignore
        latest_repo_release_api_url(owner, repo),
        *args,
        timeout=timeout,
        **kwargs,
    ).json()
