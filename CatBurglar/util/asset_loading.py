"""
A grab bag of asset loading utilities. These can be moved later if we find a
better place to keep them.
"""
import re
import errno
import os
import logging

from arcade import Texture, load_texture

LOG = logging.getLogger('arcade')

from collections import defaultdict
from pathlib import Path

# Python seems to start searching for assets from the current run directory
from typing import Union, List, Callable, Dict, Any

# Python loads from the root of the current run directory, so if assets are at
# the same directory as main.py, this will be helpful to have cached.
ASSET_BASE_PATH = Path.cwd() / "assets"

# matches files of formats like walk_left_0.png. Not currently used but may be.
SPRITE_FORMAT_REGEX_STRING = r"([A-Za-z0-9\-]+_([A-Za-z0-9\-]+))\_[0-9]+\.png"

ASSET_FILENAME_END_REGEX = re.compile(r"_([0-9]+)\.([a-zA-Z]+)$")


def validate_path_and_fetch_child_files(path: Union[Path, str]) -> List[Path]:
    """

    Validate a path as an existing file or folder, then return a list
    of either the file itself as-is or its immediate child files.

    Currently silently ignores sub-directories.

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

    # just append to output if it's a single file
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
        asset_loader: Callable,
        ignore_other_than: re.Pattern = None,
        exception_on_unexpected_filename: bool = True
) -> Dict[str, List[Any]]:
    """

    Load files to a dict of subgroup names -> lists of asset sequences.

    These dicts can then be composed through dict merging or overridden.

    The function assumes that the path passed is either a single file
    or a folder containing files matching the following name format:
        somestring_0.ext
        otherstring_0.wav
        otherstring_1.wav

    The first part before the underscore is the subgroup name. The
    number after the underscore is the sequence index.

    By default, this function will raise an exception if the sequence
    index (underscrore, number, and extension) isn't properly formed.
    You can change that to a simple logging statement by setting
    exception_on_unexpected_filename to False.

    :param raw_source: file or directory that should be loaded
    :param asset_loader: function that loads an asset from a path
    :param ignore_other_than: skip files that don't match this
    :param exception_on_unexpected_filename: whether to log or except
    :return:
    """

    # thoroughly commented so we can debug this when we inevitably break
    # it later somehow.

    # make sure this isn't an invalid path
    source = validate_path_and_fetch_child_files(raw_source)

    # temp_subgroup_dict will store Dict[str, Dict[int, Path]] with the
    # sequence index mapping to the path for the file.
    temp_subgroup_dict = defaultdict(dict)

    # the integer keys will be used to create a sorted version of the list
    # that will be stored in the final output dict.
    final_output_dict = defaultdict(list)

    # prep the filenames in unsorted order
    for file in source:

        # skip any files we don't want to load
        if ignore_other_than and not ignore_other_than.fullmatch(file.name):
            continue

        split_result = ASSET_FILENAME_END_REGEX.split(file.name)

        # The file has a malformed name if the result has the wrong length or
        # there are leftovers from the split somehow.
        if len(split_result) != 4 or split_result[3]:
            message = f"Malformed filename r{file}"

            # Depending on settings, either error or politely notify the developer.
            if exception_on_unexpected_filename:
                raise ValueError(message)
            LOG.warning(message)

        asset_subgroup_name, asset_sequence_index = split_result[0], int(split_result[1])

        # the keys of the second generated dict will be sorted below
        temp_subgroup_dict[asset_subgroup_name][asset_sequence_index] = file

    # Sort the entries in the dictionary and load them.
    # Written for easier understanding and debugging rather than conciseness.
    for subgroup_name, unsorted_entries in temp_subgroup_dict.items():

        # iterate through keys in now-sorted order and attempt to load asset
        for index in sorted(unsorted_entries.keys()):

            # attempt loading the asset
            asset = asset_loader(unsorted_entries[index])
            final_output_dict[subgroup_name].append(asset)

    # "freeze" output so it stops generating subgroup sequences
    return dict(final_output_dict)



