"""
A module implementing a configuration interface for the package.
"""

# third-party
from vcorelib.dict.codec import BasicDictCodec as _BasicDictCodec

# internal
from yambs.schemas import YambsDictCodec as _YambsDictCodec


class Config(_YambsDictCodec, _BasicDictCodec):
    """The top-level configuration object for the package."""
