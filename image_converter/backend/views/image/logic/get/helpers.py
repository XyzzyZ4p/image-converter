"""Image View get logic

This file provides helper functions to view image class
for get requests and contains the following

Functions:

    * add_extension_to_name(path: Path, data: str, extension) -> Path:
"""

from pathlib import Path


def add_extension_to_name(path: Path, data: str, extension: str) -> Path:
    """Add extension to name

    Parameters
    ----------
    path : Path
        Image file path
    data : str
        Image name
    extension : str
        Image extension

    Returns
    -------
    Path
        Full Image path with name and extension
    """
    return path / f'{data}.{extension}'
