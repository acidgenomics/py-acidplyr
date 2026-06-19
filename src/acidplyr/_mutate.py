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
    """Apply a function to all columns of a DataFrame."""
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
    """Apply a function to specific columns of a DataFrame."""
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
    """Apply a function to columns matching a predicate."""
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
    """Apply a function to specific columns, returning only those columns."""
    return mutate_all(pd.DataFrame(df[vars]), fun, *args, **kwargs)


def transmute_if(
    df: pd.DataFrame,
    predicate: Callable,
    fun: Callable,
    *args: Any,
    **kwargs: Any,
) -> pd.DataFrame:
    """Apply a function to columns matching a predicate, returning only those."""
    return mutate_all(select_if(df, predicate), fun, *args, **kwargs)
