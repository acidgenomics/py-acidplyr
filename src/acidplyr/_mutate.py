"""Mutate and transmute operations for DataFrames."""

from __future__ import annotations


import pandas as pd


def select_if(df, predicate):
    """Select columns matching a predicate (internal helper)."""
    keep = [col for col in df.columns if predicate(df[col])]
    return df[keep]


def mutate_all(df, fun, *args, **kwargs):
    """Apply a function to all columns of a DataFrame."""
    result = {}
    for col in df.columns:
        result[col] = fun(df[col], *args, **kwargs)
    out = pd.DataFrame(result, index=df.index)
    if out.shape != df.shape:
        raise ValueError("Resulting dimensions do not match input.")
    return out


def mutate_at(df, vars, fun, *args, **kwargs):
    """Apply a function to specific columns of a DataFrame."""
    mutated = transmute_at(df, vars=vars, fun=fun, *args, **kwargs)
    remaining = df[[c for c in df.columns if c not in mutated.columns]]
    out = pd.concat([mutated, remaining], axis=1)
    out = out[list(df.columns)]
    return out


def mutate_if(df, predicate, fun, *args, **kwargs):
    """Apply a function to columns matching a predicate."""
    mutated = transmute_if(df, predicate=predicate, fun=fun, *args, **kwargs)
    remaining = df[[c for c in df.columns if c not in mutated.columns]]
    out = pd.concat([mutated, remaining], axis=1)
    out = out[list(df.columns)]
    return out


def transmute_at(df, vars, fun, *args, **kwargs):
    """Apply a function to specific columns, returning only those columns."""
    subset = df[vars]
    return mutate_all(subset, fun=fun, *args, **kwargs)


def transmute_if(df, predicate, fun, *args, **kwargs):
    """Apply a function to columns matching a predicate, returning only those."""
    subset = select_if(df, predicate=predicate)
    return mutate_all(subset, fun=fun, *args, **kwargs)
