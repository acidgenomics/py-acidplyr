"""Column selection operations for DataFrames."""

from __future__ import annotations

from collections.abc import Callable

import pandas as pd


def select_if(df: pd.DataFrame, predicate: Callable) -> pd.DataFrame:
    """Select columns of a DataFrame that satisfy a predicate.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame.
    predicate : callable
        A function applied to each column (as a Series).  Columns for
        which *predicate* returns ``True`` are kept.

    Returns
    -------
    pd.DataFrame
        DataFrame containing only the selected columns.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("'df' must be a pandas DataFrame.")
    keep = [col for col in df.columns if predicate(df[col])]
    if len(keep) == 0:
        raise ValueError("No columns matched the predicate.")
    return df[keep]
