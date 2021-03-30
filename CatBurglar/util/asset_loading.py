"""
A grab bag of asset loading utilities. These can be moved later if we find a
better place to keep them.
"""
from collections import defaultdict
from pathlib import Path
import re
import errno
import os

# Python seems to start searching for assets from the current run directory
from typing import Union, DefaultDict, List, Callable

# Python loads from the root of the current run directory, so if assets are at
# the same directory as main.py, this will be helpful to have cached.
ASSET_BASE_PATH = Path.cwd() / "assets"

# matches files of formats like walk_left_0.png. Not currently used but may be.
SPRITE_FORMAT_REGEX_STRING = r"([A-Za-z0-9\-]+_([A-Za-z0-9\-]+))\_[0-9]+\.png"

SPRITE_END_NUMBER_TEMPLATE = re.compile(r"_([0-9]+)\.png$")


def validate_path_and_fetch_child_files(path: Union[Path, str]) -> List[Path]:
    """

    Validate a path as an existing file or folder, then return a list of
    either the file itself as-is or its immediate child files.

    :param path: Either a single file or a path that contains asset files
    :return: a list of paths
    """
    convenient_path = Path(path)

    if not convenient_path.exists():
        raise FileNotFoundError(
            errno.ENOENT,
            os.strerror(errno.ENOENT),
            convenient_path
        )
    processing_list = []

    if convenient_path.is_file():
        processing_list.append(convenient_path)
    elif convenient_path.is_dir():
        for child in convenient_path.iterdir():
            if child.is_file():
                processing_list.append(child)
    else:
        # I don't know of any condition where this could happen but we'll
        # raise an error if it does anyway.
        raise ValueError("Path exists but is somehow neither a file or a directory")

    return processing_list


def load_asset_group(
        raw_source: Union[Path, str],
        asset_load_function: Callable,
        only_load_matching: re.Pattern = None
) -> DefaultDict[str, List[str]]:
    """
    Utility for loading assets in paths.

    The intent is to have assets under folders with names roughly corresponding
    to classes.

    Each specific file might be named with the following format:

        animationname_direction_frameindex.extension
        footweartype_surfacetype_setidnumber.extension

    The goal is to build a dict mapping asset group names to a list of
    filenames (or loaded asset objects if asset_load_function is passed).

    These dicts can then be composed through dict merging or overridden.

    :param raw_source: a single file or raw directory that should be loaded
    :param asset_load_function: function that takes a path, returns a resource
    :return:
    """
    pass


