import os
from typing import Union


def initialize_dir(path: Union[str, bytes, os.PathLike]) -> None:
    """
    Initialize a directory at the given path.

    Parameters
    ----------
    path : Union[str, bytes, os.PathLike]
        The path to the directory to initialize.

    Returns
    -------
    None
    """
    if not os.path.exists(path):
        os.makedirs(path)


def initialize_dir_for_file(path: Union[str, bytes, os.PathLike]) -> None:
    """
    Initialize the directory for a given file path.

    Parameters
    ----------
    path : Union[str, bytes, os.PathLike]
        The path to the file.

    Returns
    -------
    None
    """
    dirname = os.path.dirname(path)
    initialize_dir(dirname)
