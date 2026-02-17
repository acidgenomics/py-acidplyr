"""Unnest (explode) list-columns in a DataFrame."""

from __future__ import annotations

import pandas as pd


def unnest2(df: pd.DataFrame, col: str) -> pd.DataFrame:
    """Explode a list-column into long format.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame.
    col : str
        Name of the column containing lists to explode.

    Returns
    -------
    pd.DataFrame
        Long-form DataFrame with one row per element.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("'df' must be a pandas DataFrame.")
    if col not in df.columns:
        raise KeyError(f"Column '{col}' not found in DataFrame.")
    is_list = df[col].apply(lambda v: isinstance(v, (list, tuple)))
    if not is_list.any():
        raise TypeError(f"Column '{col}' does not contain list values.")
    out = df.explode(col, ignore_index=True)
    return out
