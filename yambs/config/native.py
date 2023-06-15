"""
A module implementing a configuration interface for native builds.
"""

# internal
from yambs.config.common import CommonConfig
from yambs.schemas import YambsDictCodec as _YambsDictCodec


class Native(_YambsDictCodec, CommonConfig):
    """The top-level configuration object for the package."""
