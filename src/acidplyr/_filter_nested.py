"""Filter DataFrame rows by regex pattern across all columns."""

from __future__ import annotations

import re
from typing import Any

import pandas as pd


def filter_nested(
    df: pd.DataFrame,
    pattern: str,
    ignore_case: bool = False,
) -> pd.DataFrame:
    """Filter rows of a DataFrame by regex pattern across all columns.

    Searches through all columns including list-columns (nested). A row is
    kept if any value (recursively unlisted) matches the pattern.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame to filter.
    pattern : str
        Regular expression pattern to match.
    ignore_case : bool
        Whether to perform case-insensitive matching.

    Returns
    -------
    pd.DataFrame
        Filtered DataFrame containing only matching rows.
    """
    if df.empty:
        return df
    flags = re.IGNORECASE if ignore_case else 0
    compiled = re.compile(pattern, flags)
    mask = []
    for _, row in df.iterrows():
        values = _unlist_row(row)
        match = any(compiled.search(str(v)) for v in values if v is not None)
        mask.append(match)
    return df.loc[mask].reset_index(drop=True)


def _unlist_row(row: pd.Series) -> list:
    """Recursively flatten all values in a row."""
    result: list = []
    for v in row:
        result.extend(_flatten_value(v))
    return result


def _flatten_value(v: Any) -> list:
    """Recursively flatten a value (including lists/tuples)."""
    if isinstance(v, (list, tuple)):
        out: list = []
        for item in v:
            out.extend(_flatten_value(item))
        return out
    return [v]
