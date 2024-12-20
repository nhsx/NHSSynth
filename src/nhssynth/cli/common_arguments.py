"""
Functions to define the CLI's "common" arguments, i.e. those that can be applied to either:
 - All module argument lists, e.g. --dataset, --seed, etc.
 - A subset of module(s) argument lists, e.g. --synthetic, --typed, etc.
"""

import argparse
from typing import Final

from nhssynth.common.constants import TIME


def get_core_parser(overrides=False) -> argparse.ArgumentParser:
    """
    Create the core common parser group applied to all modules (and the `pipeline` and `config` options).
    Note that we leverage common titling of the argument group to ensure arguments appear together even if declared separately.

    Args:
        overrides: whether the arguments declared within are required or not.

    Returns:
        The parser with the group containing the core arguments attached.
    """
    """"""
    core = argparse.ArgumentParser(add_help=False)
    core_grp = core.add_argument_group(title="options")
    core_grp.add_argument(
        "-d",
        "--dataset",
        required=(not overrides),
        type=str,
        help="the name of the dataset to experiment with, should be present in `<DATA_DIR>`",
    )
    core_grp.add_argument(
        "-e",
        "--experiment-name",
        type=str,
        default=TIME,
        help="name the experiment run to affect logging, config, and default-behaviour i/o",
    )
    core_grp.add_argument(
        "--save-config",
        action="store_true",
        help="save the config provided via the cli, this is a recommended option for reproducibility",
    )
    return core


def get_seed_parser(overrides=False) -> argparse.ArgumentParser:
    """
    Create the common parser group for the seed.
    NB This is separate to the rest of the core arguments as it does not apply to the dashboard module.

    Args:
        overrides: whether the arguments declared within are required or not.

    Returns:
        The parser with the group containing the seed argument attached.
    """
    parser = argparse.ArgumentParser(add_help=False)
    parser_grp = parser.add_argument_group(title="options")
    parser_grp.add_argument(
        "-s",
        "--seed",
        type=int,
        help="specify a seed for reproducibility, this is a recommended option for reproducibility",
    )
    return parser


COMMON_TITLE: Final = "starting any of the following args with `_` defaults to a suffix on DATASET (e.g. `_metadata` -> `<DATASET>_metadata`);\nall filenames are relative to `experiments/<EXPERIMENT_NAME>/` unless otherwise stated"


def suffix_parser_generator(name: str, help: str, required: bool = False) -> argparse.ArgumentParser:
    """Generator function for creating parsers following a common template.
    These parsers are all suffixes to the --dataset / -d / DATASET argument, see `COMMON_TITLE`.

    Args:
        name: the name / label of the argument to add to the CLI options.
        help: the help message when the CLI is run with --help / -h.
        required: whether the argument must be provided or not.
    """

    def get_parser(overrides: bool = False) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(add_help=False)
        parser_grp = parser.add_argument_group(title=COMMON_TITLE)
        parser_grp.add_argument(
            f"--{name.replace('_', '-')}",
            required=required and not overrides,
            type=str,
            default=f"_{name}",
            help=help,
        )
        return parser

    return get_parser


COMMON_PARSERS: Final = {
    "core": get_core_parser,
    "seed": get_seed_parser,
    "metadata": suffix_parser_generator(
        "metadata",
        "filename of the metadata, NOTE that `dataloader` attempts to read this from `<DATA_DIR>`",
    ),
    "typed": suffix_parser_generator(
        "typed",
        "filename of the typed data",
    ),
    "transformed": suffix_parser_generator(
        "transformed",
        "filename of the transformed data",
    ),
    "metatransformer": suffix_parser_generator(
        "metatransformer",
        "filename of the `MetaTransformer` used to prepare the data",
    ),
    "sdv_metadata": suffix_parser_generator(
        "sdv_metadata",
        "filename of the metadata formatted for use with SDV",
    ),
    "experiments": suffix_parser_generator(
        "experiments",
        "filename of the experiment bundle, i.e. the collection of all seeds, models, and synthetic datasets",
    ),
    "synthetic_datasets": suffix_parser_generator(
        "synthetic_datasets",
        "filename of the collection of synthetic datasets generated by a given set of `experiments`",
    ),
    "model": suffix_parser_generator(
        "model",
        "name for each of the collection of models trained during a given set of `experiments`",
    ),
    "evaluations": suffix_parser_generator(
        "evaluations",
        "filename of the (collection of) evaluation(s) for a given set of `experiments`",
    ),
}
