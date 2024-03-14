# =====================================
# generator=datazen
# version=3.1.4
# hash=ce50fe613526c5b8b8b7fd8527e3566d
# =====================================

"""
yambs - Package definition for distribution.
"""

# third-party
try:
    from setuptools_wrapper.setup import setup
except (ImportError, ModuleNotFoundError):
    from yambs_bootstrap.setup import setup  # type: ignore

# internal
from yambs import DESCRIPTION, PKG_NAME, VERSION

author_info = {
    "name": "Vaughn Kottler",
    "email": "vaughnkottler@gmail.com",
    "username": "vkottler",
}
pkg_info = {
    "name": PKG_NAME,
    "slug": PKG_NAME.replace("-", "_"),
    "version": VERSION,
    "description": DESCRIPTION,
    "versions": [
        "3.11",
        "3.12",
    ],
}
setup(
    pkg_info,
    author_info,
)
