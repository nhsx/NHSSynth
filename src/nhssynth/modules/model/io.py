import argparse
import pickle
from pathlib import Path

import pandas as pd
from nhssynth.common.io import *
from nhssynth.modules.dataloader.metatransformer import MetaTransformer


def check_input_paths(
    fn_dataset: str, fn_prepared: str, fn_metatransformer: str, dir_experiment: Path
) -> tuple[str, str]:
    """
    Sets up the input and output paths for the model files.

    Args:
        fn_dataset: The base name of the dataset.
        fn_prepared: The name of the prepared data file.
        fn_metatransformer: The name of the metatransformer file.
        dir_experiment: The path to the experiment directory.

    Returns:
        The paths to the data, metadata and metatransformer files.
    """
    fn_dataset, fn_prepared, fn_metatransformer = (
        consistent_ending(fn_dataset),
        consistent_ending(fn_prepared),
        consistent_ending(fn_metatransformer),
    )
    fn_prepared, fn_metatransformer = (
        potential_suffix(fn_prepared, fn_dataset),
        potential_suffix(fn_metatransformer, fn_dataset),
    )
    warn_if_path_supplied([fn_dataset, fn_prepared, fn_metatransformer], dir_experiment)
    check_exists([fn_prepared, fn_metatransformer], dir_experiment)
    return fn_dataset, fn_prepared, fn_metatransformer


def check_output_paths(fn_dataset: Path, fn_synth: str, fn_model: str, dir_experiment: Path) -> tuple[str, str]:
    """
    Sets up the input and output paths for the model files.

    Args:
        fn_dataset: The base name of the dataset.
        fn_synth: The name of the synthetic data file.
        fn_model: The name of the model file.
        dir_experiment: The path to the experiment output directory.

    Returns:
        The path to output the model.
    """
    fn_synth, fn_model = consistent_ending(fn_synth), consistent_ending(fn_model, ".pt")
    fn_synth, fn_model = potential_suffix(fn_synth, fn_dataset), potential_suffix(fn_model, fn_dataset)
    warn_if_path_supplied([fn_synth, fn_model], dir_experiment)
    return fn_synth, fn_model


def load_required_data(
    args: argparse.Namespace, dir_experiment: Path
) -> tuple[str, pd.DataFrame, dict[str, int], MetaTransformer]:
    """
    Loads the data from `args` or from disk when the dataloader has not be run previously.

    Args:
        args: The arguments passed to the module, in this case potentially carrying the outputs of the dataloader module.
        dir_experiment: The path to the experiment directory.

    Returns:
        The data, metadata and metatransformer.
    """
    if getattr(args, "model_input", None):
        return (
            args.model_input["fn_dataset"],
            args.model_input["prepared_dataset"],
            args.model_input["metatransformer"],
        )
    else:
        fn_dataset, fn_prepared_dataset, fn_metatransformer = check_input_paths(
            args.dataset, args.prepared, args.metatransformer, dir_experiment
        )

        with open(dir_experiment / fn_prepared_dataset, "rb") as f:
            data = pickle.load(f)
        with open(dir_experiment / fn_metatransformer, "rb") as f:
            mt = pickle.load(f)

        return fn_dataset, data, mt
