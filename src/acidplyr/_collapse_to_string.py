"""Collapse values to a single string."""

import contextlib

import numpy as np
import pandas as pd


def collapse_to_string(
    obj: list | np.ndarray | pd.Series | pd.DataFrame,
    sep: str = ", ",
    sort: bool = False,
    unique: bool = False,
) -> str | pd.DataFrame:
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
        Whether to sort values before collapsing. NA values sort last
        (matches R ``sort(na.last=TRUE)``).
    unique : bool
        Whether to keep only unique values before collapsing.

    Returns
    -------
    str or pd.DataFrame
        A single collapsed string, or a single-row DataFrame.

    Notes
    -----
    Matches R's ``collapseToString`` semantics: all values (including
    ``NA``/``NaN``) are converted to strings via ``str()``; ``NA`` becomes
    the literal string ``"NA"`` rather than being silently dropped.
    """
    if isinstance(obj, pd.DataFrame):
        return _collapse_dataframe(obj, sep=sep, sort=sort, unique=unique)
    return _collapse_atomic(obj, sep=sep, sort=sort, unique=unique)


def _to_str(v: object) -> str:
    """Convert a value to string, rendering pandas NA as 'NA'."""
    is_na = False
    with contextlib.suppress(ValueError, TypeError):
        is_na = bool(pd.isna(v))
    return "NA" if is_na else str(v)


def _collapse_atomic(
    obj: list | np.ndarray | pd.Series,
    sep: str = ", ",
    sort: bool = False,
    unique: bool = False,
) -> str:
    """Collapse an atomic vector to a string.

    Matches R's ``collapseToString,atomic``: scalar inputs are returned
    as-is (as a string); no NA stripping is performed.
    """
    if not isinstance(obj, (pd.Series, np.ndarray, list, tuple)):
        return _to_str(obj)
    values = list(obj)
    if len(values) == 1:
        return _to_str(values[0])
    if unique:
        seen: list = []
        for v in values:
            if v not in seen:
                seen.append(v)
        values = seen
    if sort:
        # NA/None values sort last (R: sort(na.last=TRUE))
        def _sort_key(v: object) -> tuple:
            na = False
            with contextlib.suppress(ValueError, TypeError):
                na = bool(pd.isna(v))
            return (na, str(v))

        values = sorted(values, key=_sort_key)
    return sep.join(_to_str(v) for v in values)


def _collapse_dataframe(
    obj: pd.DataFrame,
    sep: str = ", ",
    sort: bool = False,
    unique: bool = False,
) -> pd.DataFrame:
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
