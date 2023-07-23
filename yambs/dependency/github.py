"""
A module implementing GitHub dependency interactions.
"""

# built-in
from typing import Dict

# third-party
from vcorelib.logging import LoggerMixin

# internal
from yambs.github import latest_release_data


class GithubDependency(LoggerMixin):
    """A class for managing GitHub dependencies."""

    def __init__(self, owner: str, repo: str, *args, **kwargs) -> None:
        """Initialize this instance."""

        super().__init__(logger_name=f"{owner}.{repo}")
        self.data = latest_release_data(owner, repo, *args, **kwargs)

        self.logger.info(
            "Loaded release '%s' (%s).",
            self.data["name"],
            self.data["html_url"],
        )

        # Collect URLs for release content.
        self.download_urls: Dict[str, str] = {
            item["name"]: item["browser_download_url"]
            for item in self.data["assets"]
        }
