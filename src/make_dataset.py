"""
make_dataset module - functions to create the data.

TODO: 
  Make this a data class
  Generally tidy this up
"""

import numpy as np
import pandas as pd


def make_dataset_from_raw(path: str):
    """
    Creates a clean data frame with corrected absorption from raw CSV.

    Args:
        path: Path to the data data to be read in.

    Returns:
        Returns (data, file info) tuple.

    """
    # CSV not in standard UTF-8 so specify encoding
    with open(path, "r", encoding="utf-8-sig") as f:
        # set default file info
        file_info = {
            "user": "",
            "path": "",
            "test_id": "",
            "test_name": "",
            "date": "",
            "time": "",
            "description": "",
        }
        # header info only up to line 6
        for i, line in enumerate(f.readlines()[:7]):
            # filter line to only parts with value
            info_items = [val for val in line.split(",") if val]
            info_items = [val for val in info_items if val != "\n"]
            for item in info_items:
                if ":" in item:
                    k, v = item.split(":", 1)
                    # assign data to info dict
                    #  if key not there, it will add it
                    file_info[k.lower().replace(" ", "_")] = v.strip()
                else:
                    # if no tag found, concatenate to description
                    file_info["description"] += " " + item + "."

    df_raw = pd.read_csv(path, header=10)
    id_cols = [col for col in df_raw.columns if not col.isnumeric()]
    data_cols = [col for col in df_raw.columns if col.isnumeric()]
    df_raw = df_raw.melt(
        id_vars=id_cols,
        value_vars=data_cols,
        var_name="wavelength_nm",
        value_name="absorption_od",
    )
    # rename columns for consistency
    df_raw.columns = [col.lower().replace(" ", "_") for col in df_raw.columns]

    ###
    # Reshape and perform calculations
    ###

    # split sample from blank
    #    TODO: make this more robust
    df_sample = df_raw.loc[df_raw["sample"] != "Blank"].copy()
    df_blank = df_raw.loc[df_raw["sample"] == "Blank"].copy()

    # average multiple measurements
    #  note "Well" info is lost upon aggregation
    df_sample = (
        df_sample.groupby(["sample", "dilution", "wavelength_nm"])["absorption_od"]
        .agg(["mean", "std"])
        .reset_index()
        .rename({"mean": "mean_absorption", "std": "absorption_std"}, axis=1)
    )

    df_blank = (
        df_blank.groupby(["sample", "dilution", "wavelength_nm"])["absorption_od"]
        .agg(["mean", "std"])
        .reset_index()
        .rename({"mean": "mean_absorption", "std": "absorption_std"}, axis=1)
    )

    df = pd.merge(
        left=df_sample,
        right=df_blank,
        on="wavelength_nm",
        suffixes=["_sample", "_blank"],
    )

    # calculate corrected absorption with error
    #   ref for error calc:
    #   https://faraday.physics.utoronto.ca/PVB/Harrison/ErrorAnalysis/Propagation.html
    df["corrected_mean_absorption_sample"] = (
        df["mean_absorption_sample"] - df["mean_absorption_blank"]
    )
    df["corrected_absorption_std_sample"] = np.sqrt(
        (df["absorption_std_sample"] ** 2 + df["absorption_std_blank"] ** 2)
    )

    return df, file_info
