"""Join operations for pandas DataFrames."""

from __future__ import annotations

import pandas as pd


def _check_by_columns_exist(
    x: pd.DataFrame,
    y: pd.DataFrame,
    by: list[str],
) -> None:
    """Check that all 'by' columns exist in both DataFrames."""
    for col in by:
        if col not in x.columns:
            raise ValueError(f"Column '{col}' not found in 'x'.")
        if col not in y.columns:
            raise ValueError(f"Column '{col}' not found in 'y'.")


def _check_by_constraints(
    df: pd.DataFrame,
    by: list[str],
    *,
    label: str,
    require_unique: bool,
    require_complete: bool,
) -> None:
    """Check uniqueness and completeness constraints on 'by' columns."""
    if require_unique and df[by].duplicated().any():
        raise ValueError(f"Columns defined in 'by' argument are not unique in '{label}'.")
    if require_complete and df[by].isna().any().any():
        raise ValueError(f"Columns defined in 'by' argument contain NA in '{label}'.")


def _validate_join_args(
    x: pd.DataFrame,
    y: pd.DataFrame,
    by: str | list[str],
    *,
    require_x_unique: bool = True,
    require_y_unique: bool = True,
    require_x_complete: bool = True,
    require_y_complete: bool = True,
) -> list[str]:
    """Validate common join arguments and return 'by' as a list."""
    by = [by] if isinstance(by, str) else list(by)
    if len(by) != len(set(by)):
        raise ValueError("'by' columns must not contain duplicates.")
    _check_by_columns_exist(x, y, by)
    x_extra = set(x.columns) - set(by)
    y_extra = set(y.columns) - set(by)
    overlap = x_extra & y_extra
    if overlap:
        raise ValueError(f"Non-key columns overlap between 'x' and 'y': {overlap}.")
    _check_by_constraints(
        y, by, label="y", require_unique=require_y_unique, require_complete=require_y_complete
    )
    _check_by_constraints(
        x, by, label="x", require_unique=require_x_unique, require_complete=require_x_complete
    )
    return by


def inner_join(
    x: pd.DataFrame,
    y: pd.DataFrame,
    by: str | list[str],
) -> pd.DataFrame:
    """Inner join: return rows present in both x and y."""
    by = _validate_join_args(x, y, by)
    out = pd.merge(x, y, on=by, how="inner", sort=False)
    out = out.reset_index(drop=True)
    return out


def left_join(
    x: pd.DataFrame,
    y: pd.DataFrame,
    by: str | list[str],
) -> pd.DataFrame:
    """Left join: return all rows from x, matching rows from y."""
    by_list = [by] if isinstance(by, str) else list(by)
    if len(by_list) != len(set(by_list)):
        raise ValueError("'by' columns must not contain duplicates.")
    _check_by_columns_exist(x, y, by_list)
    x_extra = set(x.columns) - set(by_list)
    y_extra = set(y.columns) - set(by_list)
    overlap = x_extra & y_extra
    if overlap:
        raise ValueError(f"Non-key columns overlap between 'x' and 'y': {overlap}.")
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


def right_join(
    x: pd.DataFrame,
    y: pd.DataFrame,
    by: str | list[str],
) -> pd.DataFrame:
    """Right join: equivalent to left_join(y, x, by)."""
    return left_join(x=y, y=x, by=by)


def full_join(
    x: pd.DataFrame,
    y: pd.DataFrame,
    by: str | list[str],
) -> pd.DataFrame:
    """Full (outer) join: return all rows from both x and y."""
    by = _validate_join_args(x, y, by)
    out = pd.merge(x, y, on=by, how="outer", sort=False)
    out = out.reset_index(drop=True)
    return out


def semi_join(
    x: pd.DataFrame,
    y: pd.DataFrame,
    by: str | list[str],
) -> pd.DataFrame:
    """Semi join: return rows from x that have matches in y."""
    by = _validate_join_args(x, y, by)
    merged = pd.merge(x, y[by], on=by, how="inner", sort=False)
    # Keep only x columns and deduplicate
    out = merged[list(x.columns)].drop_duplicates().reset_index(drop=True)
    return out


def anti_join(
    x: pd.DataFrame,
    y: pd.DataFrame,
    by: str | list[str],
) -> pd.DataFrame:
    """Anti join: return rows from x that have no match in y."""
    by = _validate_join_args(x, y, by)
    indicator = pd.merge(x, y[by], on=by, how="left", indicator=True, sort=False)
    mask = indicator["_merge"] == "left_only"
    out = x.loc[mask.values].reset_index(drop=True)
    return out
