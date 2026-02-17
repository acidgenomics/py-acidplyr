"""Join operations for pandas DataFrames."""

from __future__ import annotations


import pandas as pd


def _validate_join_args(
    x,
    y,
    by,
    *,
    require_x_unique=True,
    require_y_unique=True,
    require_x_complete=True,
    require_y_complete=True,
):
    """Validate common join arguments and return 'by' as a list."""
    if isinstance(by, str):
        by = [by]
    else:
        by = list(by)
    if len(by) != len(set(by)):
        raise ValueError("'by' columns must not contain duplicates.")
    for col in by:
        if col not in x.columns:
            raise ValueError(f"Column '{col}' not found in 'x'.")
        if col not in y.columns:
            raise ValueError(f"Column '{col}' not found in 'y'.")
    x_extra = set(x.columns) - set(by)
    y_extra = set(y.columns) - set(by)
    overlap = x_extra & y_extra
    if overlap:
        raise ValueError(
            f"Non-key columns overlap between 'x' and 'y': {overlap}."
        )
    if require_y_unique:
        if y[by].duplicated().any():
            raise ValueError(
                "Columns defined in 'by' argument are not unique in 'y'."
            )
    if require_x_unique:
        if x[by].duplicated().any():
            raise ValueError(
                "Columns defined in 'by' argument are not unique in 'x'."
            )
    if require_y_complete:
        if y[by].isna().any().any():
            raise ValueError(
                "Columns defined in 'by' argument contain NA in 'y'."
            )
    if require_x_complete:
        if x[by].isna().any().any():
            raise ValueError(
                "Columns defined in 'by' argument contain NA in 'x'."
            )
    return by


def inner_join(x, y, by):
    """Inner join: return rows present in both x and y."""
    by = _validate_join_args(x, y, by)
    out = pd.merge(x, y, on=by, how="inner", sort=False)
    out = out.reset_index(drop=True)
    return out


def left_join(x, y, by):
    """Left join: return all rows from x, matching rows from y."""
    by_list = [by] if isinstance(by, str) else list(by)
    if len(by_list) != len(set(by_list)):
        raise ValueError("'by' columns must not contain duplicates.")
    for col in by_list:
        if col not in x.columns:
            raise ValueError(f"Column '{col}' not found in 'x'.")
        if col not in y.columns:
            raise ValueError(f"Column '{col}' not found in 'y'.")
    x_extra = set(x.columns) - set(by_list)
    y_extra = set(y.columns) - set(by_list)
    overlap = x_extra & y_extra
    if overlap:
        raise ValueError(
            f"Non-key columns overlap between 'x' and 'y': {overlap}."
        )
    if y[by_list].duplicated().any():
        raise ValueError("Columns defined in 'by' argument are not unique.")
    if y[by_list].isna().any().any():
        raise ValueError("Columns defined in 'by' argument contain NA.")
    original_order = x.index.copy()
    out = pd.merge(x, y, on=by_list, how="left", sort=False)
    if len(out) > len(x):
        out = out.drop_duplicates(subset=list(x.columns), keep="first")
        if len(out) > len(x):
            out = out.head(len(x))
    out.index = original_order
    return out


def right_join(x, y, by):
    """Right join: equivalent to left_join(y, x, by)."""
    return left_join(x=y, y=x, by=by)


def full_join(x, y, by):
    """Full (outer) join: return all rows from both x and y."""
    by = _validate_join_args(x, y, by)
    out = pd.merge(x, y, on=by, how="outer", sort=False)
    out = out.reset_index(drop=True)
    return out


def semi_join(x, y, by):
    """Semi join: return rows from x that have matches in y."""
    by = _validate_join_args(x, y, by)
    merged = pd.merge(x, y[by], on=by, how="inner", sort=False)
    # Keep only x columns and deduplicate
    out = merged[list(x.columns)].drop_duplicates().reset_index(drop=True)
    return out


def anti_join(x, y, by):
    """Anti join: return rows from x that have no match in y."""
    by = _validate_join_args(x, y, by)
    indicator = pd.merge(
        x, y[by], on=by, how="left", indicator=True, sort=False
    )
    mask = indicator["_merge"] == "left_only"
    out = x.loc[mask.values].reset_index(drop=True)
    return out
