"""Melt (unpivot) a matrix or DataFrame from wide to long format."""

from __future__ import annotations

from typing import Optional, Union

import numpy as np
import pandas as pd


def melt(
    obj: Union[np.ndarray, pd.DataFrame],
    colnames: Optional[list] = None,
    min: Optional[float] = None,
    min_method: str = "absolute",
    trans: str = "identity",
) -> pd.DataFrame:
    """Melt (unpivot) a matrix or DataFrame from wide to long format.

    Parameters
    ----------
    obj : np.ndarray or pd.DataFrame
        Wide-format data to melt.
    colnames : list of str or None
        Column names to include in the melt. If None, all columns are used.
    min : float or None
        Minimum value threshold (>= logic). None to disable.
    min_method : str
        "absolute" or "perRow".
    trans : str
        "identity", "log2", or "log10". Applies trans(x + 1).

    Returns
    -------
    pd.DataFrame
        Long-format DataFrame with columns: rowname, colname, value.
    """
    if min_method not in ("absolute", "perRow"):
        raise ValueError("'min_method' must be 'absolute' or 'perRow'.")
    if trans not in ("identity", "log2", "log10"):
        raise ValueError("'trans' must be 'identity', 'log2', or 'log10'.")
    if isinstance(obj, pd.DataFrame):
        if colnames is not None:
            obj = obj[colnames]
        row_names = list(obj.index.astype(str))
        col_names = list(obj.columns.astype(str))
        mat = obj.values
    elif isinstance(obj, np.ndarray):
        mat = obj
        row_names = None
        col_names = None
    else:
        raise TypeError(f"Unsupported type: {type(obj)}")
    if mat.ndim != 2:
        raise ValueError("Input must be 2-dimensional.")
    nrow, ncol = mat.shape
    if row_names is None:
        row_names = [str(i + 1) for i in range(nrow)]
    if col_names is None:
        col_names = [str(i + 1) for i in range(ncol)]
    if min_method == "perRow" and min is not None and np.isfinite(min):
        row_sums = np.nansum(mat, axis=1)
        keep = row_sums >= min
        mat = mat[keep, :]
        row_names = [row_names[i] for i, k in enumerate(keep) if k]
        nrow = mat.shape[0]
    row_vals = []
    col_vals = []
    value_vals = []
    for ci in range(ncol):
        for ri in range(nrow):
            row_vals.append(row_names[ri])
            col_vals.append(col_names[ci])
            value_vals.append(mat[ri, ci])
    df = pd.DataFrame(
        {
            "rowname": pd.Categorical(row_vals, categories=row_names),
            "colname": pd.Categorical(col_vals, categories=col_names),
            "value": value_vals,
        }
    )
    if min_method == "absolute" and min is not None and np.isfinite(min):
        df = df[df["value"] >= min].reset_index(drop=True)
    if trans == "log2":
        df["value"] = np.log2(df["value"].astype(float) + 1)
    elif trans == "log10":
        df["value"] = np.log10(df["value"].astype(float) + 1)
    return df
