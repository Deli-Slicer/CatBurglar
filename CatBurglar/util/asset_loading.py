"""
A grab bag of asset loading utilities. These can be moved later if we find a
better place to keep them.
"""
from pathlib import Path

# Python seems to start searching for assets from the current run directory
from typing import Union, DefaultDict, List, Callable

# Python loads from the root of the current run directory, so if assets are at
# the same directory as main.py, this will be helpful to have cached.
ASSET_BASE_PATH = Path.cwd() / "assets"

# matches files of formats like walk_left_0.png. Not currently used but may be.
SPRITE_FORMAT_REGEX_STRING = r"([A-Za-z0-9\-]+_([A-Za-z0-9\-]+))\_[0-9]+\.png"

def load_asset_group(
        source_dir: Union[Path, str],
        filename_regex: str = None,
        asset_load_function: Callable  = None
) -> DefaultDict[str, List[str]]:
    """
    Utility for loading assets in paths.

    The intent is have assets under folders with names roughly corresponding
    to classes.

    Each specific file might be named with the following format:

        animationname_direction_frameindex.extension
        footweartype_surfacetype_setidnumber.extension

    The goal is to build a dict mapping asset group names to a list of
    filenames (or loaded asset objects if asset_load_function is passed).

    These dicts can then be composed through dict merging or overridden.

    :param source_dir: what the directory of this asset group is
    :param filename_regex: a regex to filter the results if any
    :param asset_load_function: function that takes a path, returns a resource
    :return:
    """
    # todo: implement this if we end up needing it
    pass

