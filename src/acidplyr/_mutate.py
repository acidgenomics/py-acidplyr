"""Mutate and transmute operations for DataFrames."""

from collections.abc import Callable
from typing import Any

import pandas as pd

from acidplyr._select import select_if


def mutate_all(
    df: pd.DataFrame,
    fun: Callable,
    *args: Any,
    **kwargs: Any,
) -> pd.DataFrame:
    """Apply a function to all columns of a DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame.
    fun : callable
        Function applied to each column (as a Series). Must return a
        Series or array of the same length.
    *args
        Additional positional arguments passed to ``fun``.
    **kwargs
        Additional keyword arguments passed to ``fun``.

    Returns
    -------
    pd.DataFrame
        DataFrame with every column replaced by ``fun``'s output. Raises
        if the result's shape doesn't match ``df``.

    Examples
    --------
    >>> import pandas as pd
    >>> df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
    >>> mutate_all(df, lambda s: s * 2).to_dict("list")
    {'a': [2, 4], 'b': [6, 8]}
    """
    result = {}
    for col in df.columns:
        result[col] = fun(df[col], *args, **kwargs)
    out = pd.DataFrame(result, index=df.index)
    if out.shape != df.shape:
        raise ValueError("Resulting dimensions do not match input.")
    return out


def mutate_at(
    df: pd.DataFrame,
    vars: list[str],
    fun: Callable,
    *args: Any,
    **kwargs: Any,
) -> pd.DataFrame:
    """Apply a function to specific columns of a DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame.
    vars : list of str
        Column names to transform. Other columns pass through unchanged.
    fun : callable
        Function applied to each selected column (as a Series).
    *args
        Additional positional arguments passed to ``fun``.
    **kwargs
        Additional keyword arguments passed to ``fun``.

    Returns
    -------
    pd.DataFrame
        DataFrame with all original columns; ``vars`` columns replaced by
        ``fun``'s output, in the original column order.

    Examples
    --------
    >>> import pandas as pd
    >>> df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
    >>> mutate_at(df, ["a"], lambda s: s * 2).to_dict("list")
    {'a': [2, 4], 'b': [3, 4]}
    """
    mutated = transmute_at(df, vars, fun, *args, **kwargs)
    remaining = df[[c for c in df.columns if c not in mutated.columns]]
    out = pd.DataFrame(pd.concat([mutated, remaining], axis=1))
    return pd.DataFrame(out[list(df.columns)])


def mutate_if(
    df: pd.DataFrame,
    predicate: Callable,
    fun: Callable,
    *args: Any,
    **kwargs: Any,
) -> pd.DataFrame:
    """Apply a function to columns matching a predicate.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame.
    predicate : callable
        Function applied to each column (as a Series); columns for which
        it returns ``True`` are transformed.
    fun : callable
        Function applied to each matching column.
    *args
        Additional positional arguments passed to ``fun``.
    **kwargs
        Additional keyword arguments passed to ``fun``.

    Returns
    -------
    pd.DataFrame
        DataFrame with all original columns; matching columns replaced by
        ``fun``'s output, in the original column order.

    Examples
    --------
    >>> import pandas as pd
    >>> df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
    >>> mutate_if(df, lambda s: s.name == "a", lambda s: s * 10).to_dict("list")
    {'a': [10, 20], 'b': [3, 4]}
    """
    mutated = transmute_if(df, predicate, fun, *args, **kwargs)
    remaining = df[[c for c in df.columns if c not in mutated.columns]]
    out = pd.DataFrame(pd.concat([mutated, remaining], axis=1))
    return pd.DataFrame(out[list(df.columns)])


def transmute_at(
    df: pd.DataFrame,
    vars: list[str],
    fun: Callable,
    *args: Any,
    **kwargs: Any,
) -> pd.DataFrame:
    """Apply a function to specific columns, returning only those columns.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame.
    vars : list of str
        Column names to transform and return.
    fun : callable
        Function applied to each selected column (as a Series).
    *args
        Additional positional arguments passed to ``fun``.
    **kwargs
        Additional keyword arguments passed to ``fun``.

    Returns
    -------
    pd.DataFrame
        DataFrame containing only the transformed ``vars`` columns.

    Examples
    --------
    >>> import pandas as pd
    >>> df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
    >>> transmute_at(df, ["a"], lambda s: s * 2).to_dict("list")
    {'a': [2, 4]}
    """
    return mutate_all(pd.DataFrame(df[vars]), fun, *args, **kwargs)


def transmute_if(
    df: pd.DataFrame,
    predicate: Callable,
    fun: Callable,
    *args: Any,
    **kwargs: Any,
) -> pd.DataFrame:
    """Apply a function to columns matching a predicate, returning only those.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame.
    predicate : callable
        Function applied to each column (as a Series); columns for which
        it returns ``True`` are transformed and returned.
    fun : callable
        Function applied to each matching column.
    *args
        Additional positional arguments passed to ``fun``.
    **kwargs
        Additional keyword arguments passed to ``fun``.

    Returns
    -------
    pd.DataFrame
        DataFrame containing only the transformed matching columns.

    Examples
    --------
    >>> import pandas as pd
    >>> df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
    >>> transmute_if(df, lambda s: s.name == "a", lambda s: s * 10).to_dict(
    ...     "list"
    ... )
    {'a': [10, 20]}
    """
    return mutate_all(select_if(df, predicate), fun, *args, **kwargs)
