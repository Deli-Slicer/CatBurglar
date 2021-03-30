"""
Asset loading type shorthands, constants, and assistance functions.
"""
import errno
import os
import re
import logging
from collections import defaultdict
from pathlib import Path
from arcade import Texture, load_texture
from typing import Union, List, Callable, Dict, Any, Iterable, Mapping

LOG = logging.getLogger('arcade')

# Describes anything that maps strings to lists of textures. Used
# elsewhere in the project as well.
AnimationStateDict = Mapping[str, List[Texture]]

# Python loads from the root of the current run directory, so if assets
# are at the root of the project, this will be helpful to have cached.
ASSET_BASE_PATH = Path.cwd() / "assets"

# matches files of formats like walk_left_0.png. Not currently used
# but can be passed to one of the functions below that takes regexes.
SPRITE_FORMAT_REGEX_STRING = r"([A-Za-z0-9\-]+_([A-Za-z0-9\-]+))\_[0-9]+\.png"

# helps check sequence formation for animations and other sequences
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

    # fetch all file children
    elif convenient_path.is_dir():
        for child in convenient_path.iterdir():
            if child.is_file():
                processing_list.append(child)
    else:
        # I don't know of any condition where this could happen but we'll
        # raise an error if it does anyway.
        raise ValueError("Path exists but is somehow neither a file or a directory")

    return processing_list


class AssetGroupError(Exception):
    """
    For problems loading files other than corrupted or non-accessible files.
    """
    def __init__(self, message: str, subgroup: str):
        self.message = message
        self.subgroup = subgroup
        super().__init__(message)


class MissingSequenceMember(AssetGroupError):
    """
    When there is a missing asset in a sequence
    """
    def __init__(
            self,
            message: str,
            subgroup: str,
            last_good_index: int,
            bad: int
    ):
        super(MissingSequenceMember, self).__init__(message, subgroup)
        self.last_good_index = last_good_index
        self.bad = bad


class MissingSubgroup(AssetGroupError):
    """
    When a subgroup was expected but isn't found
    """
    def __init__(self, message: str, subgroup: str):
        super().__init__(message, subgroup)


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
    final_ordering = defaultdict(list)

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
        previous = -1

        for index in sorted(unsorted_entries.keys()):
            if previous != index - 1:
                message =\
                    f"Malformed asset sequence for subgroup {subgroup_name!r}:"\
                    f" sequence break between index {previous!r} and {index!r}"

                if exception_on_unexpected_filename:
                    raise MissingSequenceMember(
                        message,
                        subgroup_name,
                        previous,
                        index
                    )
                else:
                    LOG.warning(message)

            previous = index

            # attempt loading the asset
            asset = asset_loader(unsorted_entries[index])
            final_ordering[subgroup_name].append(asset)

    # "freeze" output so it stops generating subgroup sequences
    return dict(final_ordering)


def preload_entity_texture_table(
        path: Union[Path, str],
        required_state_subgroups: Iterable[str]
) -> Dict[str, List[Texture]]:
    """
    Convenience method around load_asset_group for loading textures.

    Will Raise an AssetError if a state passed as required is missing.

    :param path: a path to load textures from
    :param required_state_subgroups: list of subgroups to ensure
    :return:
    """

    output = load_asset_group(
        path,
        load_texture
    )
    for state in required_state_subgroups:
        if state not in output:
            raise MissingSubgroup(f"Missing subgroup member: {state!r} in {path!r}", state)

    return output

