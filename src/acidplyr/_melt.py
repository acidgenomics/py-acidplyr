"""Melt (unpivot) a matrix or DataFrame from wide to long format."""

from __future__ import annotations

import numpy as np
import pandas as pd


def _parse_melt_input(
    obj: np.ndarray | pd.DataFrame,
    colnames: list | None,
) -> tuple[np.ndarray, list[str] | None, list[str] | None]:
    """Parse and validate melt input, returning matrix and names."""
    if isinstance(obj, pd.DataFrame):
        if colnames is not None:
            obj = obj[colnames]
        row_names = list(obj.index.astype(str))
        col_names = list(obj.columns.astype(str))
        return obj.values, row_names, col_names
    if isinstance(obj, np.ndarray):
        return obj, None, None
    raise TypeError(f"Unsupported type: {type(obj)}")


def _apply_row_filter(
    mat: np.ndarray,
    row_names: list[str],
    min_val: float,
) -> tuple[np.ndarray, list[str]]:
    """Filter rows by per-row sum threshold."""
    row_sums = np.nansum(mat, axis=1)
    keep = row_sums >= min_val
    mat = mat[keep, :]
    row_names = [row_names[i] for i, k in enumerate(keep) if k]
    return mat, row_names


def _build_long_df(
    mat: np.ndarray,
    row_names: list[str],
    col_names: list[str],
) -> pd.DataFrame:
    """Build long-format DataFrame from matrix and names."""
    nrow, ncol = mat.shape
    row_vals = []
    col_vals = []
    value_vals = []
    for ci in range(ncol):
        for ri in range(nrow):
            row_vals.append(row_names[ri])
            col_vals.append(col_names[ci])
            value_vals.append(mat[ri, ci])
    return pd.DataFrame(
        {
            "rowname": pd.Categorical(row_vals, categories=row_names),
            "colname": pd.Categorical(col_vals, categories=col_names),
            "value": value_vals,
        }
    )


def melt(
    obj: np.ndarray | pd.DataFrame,
    colnames: list | None = None,
    min: float | None = None,
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
    mat, row_names, col_names = _parse_melt_input(obj, colnames)
    if mat.ndim != 2:
        raise ValueError("Input must be 2-dimensional.")
    nrow, ncol = mat.shape
    if row_names is None:
        row_names = [str(i + 1) for i in range(nrow)]
    if col_names is None:
        col_names = [str(i + 1) for i in range(ncol)]
    if min_method == "perRow" and min is not None and np.isfinite(min):
        mat, row_names = _apply_row_filter(mat, row_names, min)
    df = _build_long_df(mat, row_names, col_names)
    if min_method == "absolute" and min is not None and np.isfinite(min):
        df = df[df["value"] >= min].reset_index(drop=True)
    if trans == "log2":
        df["value"] = np.log2(df["value"].astype(float) + 1)
    elif trans == "log10":
        df["value"] = np.log10(df["value"].astype(float) + 1)
    return df
