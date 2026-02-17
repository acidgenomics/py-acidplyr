"""Unlist a dictionary of DataFrames into a single DataFrame."""

from __future__ import annotations

import pandas as pd


def unlist2(x, name_col="name", rowname_col="rowname"):
    """Unlist a dictionary of DataFrames into a single DataFrame.

    Unlike ``pd.concat``, this adds explicit *name_col* and *rowname_col*
    columns instead of using a MultiIndex.

    Parameters
    ----------
    x : dict[str, pd.DataFrame]
        Named dictionary of DataFrames.
    name_col : str, optional
        Column name for the dictionary keys.
    rowname_col : str, optional
        Column name for the original row indices.

    Returns
    -------
    pd.DataFrame
    """
    if not isinstance(x, dict):
        raise TypeError("'x' must be a dict.")
    if len(x) == 0:
        raise ValueError("'x' has length 0.")
    frames = []
    for key, df in x.items():
        if not isinstance(df, pd.DataFrame):
            raise TypeError(f"Element '{key}' is not a DataFrame.")
        tmp = df.copy()
        tmp[name_col] = key
        tmp[rowname_col] = [str(i) for i in tmp.index]
        frames.append(tmp)
    out = pd.concat(frames, ignore_index=True)
    cols = [name_col, rowname_col] + [
        c for c in out.columns if c not in (name_col, rowname_col)
    ]
    return out[cols]
