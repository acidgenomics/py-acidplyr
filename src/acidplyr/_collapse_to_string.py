"""Collapse values to a single string."""

from __future__ import annotations

from typing import Union

import numpy as np
import pandas as pd


def collapse_to_string(
    obj: Union[list, np.ndarray, pd.Series, pd.DataFrame],
    sep: str = ", ",
    sort: bool = False,
    unique: bool = False,
) -> Union[str, pd.DataFrame]:
    """Collapse values to a delimited string.

    For atomic/list inputs, returns a single string. For DataFrame inputs,
    collapses each column to a single row.

    Parameters
    ----------
    obj : list, np.ndarray, pd.Series, or pd.DataFrame
        Input to collapse.
    sep : str
        Separator string.
    sort : bool
        Whether to sort values before collapsing.
    unique : bool
        Whether to keep only unique values before collapsing.

    Returns
    -------
    str or pd.DataFrame
        A single collapsed string, or a single-row DataFrame.
    """
    if isinstance(obj, pd.DataFrame):
        return _collapse_dataframe(obj, sep=sep, sort=sort, unique=unique)
    return _collapse_atomic(obj, sep=sep, sort=sort, unique=unique)


def _is_na_like(v):
    """Check if value is NA/NaN/None-like."""
    if v is None:
        return True
    if isinstance(v, float) and np.isnan(v):
        return True
    try:
        if pd.isna(v):
            return True
    except ValueError, TypeError:
        pass
    return False


def _collapse_atomic(obj, sep=", ", sort=False, unique=False):
    """Collapse an atomic vector to a string."""
    if isinstance(obj, (pd.Series, np.ndarray)):
        values = list(obj)
    elif isinstance(obj, (list, tuple)):
        values = list(obj)
    else:
        return str(obj)
    # Remove NA/None values.
    values = [v for v in values if not _is_na_like(v)]
    if len(values) <= 1:
        if len(values) == 1:
            return str(values[0])
        return ""
    if unique:
        seen = []
        for v in values:
            if v not in seen:
                seen.append(v)
        values = seen
    if sort:
        values = sorted(values, key=lambda x: str(x))
    parts = [str(v) for v in values]
    return sep.join(parts)


def _collapse_dataframe(obj, sep=", ", sort=False, unique=False):
    """Collapse a DataFrame to a single-row DataFrame."""
    if obj.empty:
        raise ValueError("Object has no length.")
    result = {}
    for col in obj.columns:
        result[col] = _collapse_atomic(
            list(obj[col]),
            sep=sep,
            sort=sort,
            unique=unique,
        )
    return pd.DataFrame(result, index=[0])
