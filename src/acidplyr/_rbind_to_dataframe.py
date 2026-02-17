"""Bind nested dictionaries into a DataFrame."""

from __future__ import annotations

import numpy as np
import pandas as pd


def rbind_to_dataframe(x):
    """Convert a named dictionary of dictionaries to a DataFrame.

    Parameters
    ----------
    x : dict
        A dictionary whose values are themselves dictionaries (or similar
        mapping objects).  Each inner dictionary becomes a row in the
        resulting DataFrame.

    Returns
    -------
    pd.DataFrame
        A DataFrame with one row per key of *x*.
    """
    if not isinstance(x, dict):
        raise TypeError("'x' must be a dict.")
    if len(x) == 0:
        raise ValueError("'x' has length 0.")
    rows = {}
    for key, val in x.items():
        if isinstance(val, dict):
            rows[key] = val
        else:
            rows[key] = {"value": val}
    df = pd.DataFrame.from_dict(rows, orient="index")
    for col in df.columns:
        if df[col].apply(lambda v: isinstance(v, (list, np.ndarray))).any():
            continue
        try:
            df[col] = pd.to_numeric(df[col])
        except (ValueError, TypeError):
            pass
    return df
