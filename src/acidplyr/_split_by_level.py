"""Split a DataFrame by factor (Categorical) levels."""

from __future__ import annotations

import pandas as pd


def split_by_level(df, f, ref=False):
    """Split a DataFrame by the levels of a Categorical column.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame.
    f : str
        Name of a column that has ``pd.Categorical`` dtype.
    ref : bool, optional
        If ``True``, include the reference (first) level in every split
        group.  Default is ``False``.

    Returns
    -------
    dict[str, pd.DataFrame]
        A dictionary keyed by level name.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("'df' must be a pandas DataFrame.")
    if f not in df.columns:
        raise KeyError(f"Column '{f}' not found in DataFrame.")
    col = df[f]
    if not hasattr(col, "cat"):
        raise TypeError(f"Column '{f}' is not Categorical.")
    levels = list(col.cat.categories)
    if len(levels) < 2:
        raise ValueError("Column must have at least 2 levels.")
    ref_level = levels[0]
    out = {}
    for lvl in levels:
        if ref and lvl != ref_level:
            mask = col.isin([ref_level, lvl])
        else:
            mask = col == lvl
        subset = df.loc[mask].copy()
        subset[f] = subset[f].cat.remove_unused_categories()
        out[lvl] = subset
    return out
