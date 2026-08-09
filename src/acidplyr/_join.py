"""Join operations for pandas DataFrames."""

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


def _check_by_dtypes_match(
    x: pd.DataFrame,
    y: pd.DataFrame,
    by: list[str],
) -> None:
    """Check that 'by' column dtypes are identical between x and y.

    Mismatched dtypes (e.g. int vs float, str vs category) silently produce
    wrong merge results in pandas — R asserts class identity here.
    """
    for col in by:
        xd = x[col].dtype
        yd = y[col].dtype
        if xd != yd:
            raise TypeError(f"Column '{col}' dtype mismatch: x has {xd!r}, y has {yd!r}.")


def _check_by_constraints(
    df: pd.DataFrame,
    by: list[str],
    *,
    label: str,
    require_unique: bool,
    require_complete: bool,
) -> None:
    """Check uniqueness and completeness constraints on 'by' columns."""
    sub = pd.DataFrame(df[by])
    if require_unique and bool(sub.duplicated().any()):
        raise ValueError(f"Columns defined in 'by' argument are not unique in '{label}'.")
    if require_complete and bool(sub.isna().any(axis=None)):
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
    _check_by_dtypes_match(x, y, by)
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
    """Inner join: return rows present in both x and y.

    Parameters
    ----------
    x : pd.DataFrame
        Left DataFrame.
    y : pd.DataFrame
        Right DataFrame.
    by : str or list of str
        Column name(s) to join on. Must exist in both ``x`` and ``y`` with
        matching dtypes.

    Returns
    -------
    pd.DataFrame
        Rows from ``x`` and ``y`` whose ``by`` values match, in ``x`` order.

    Examples
    --------
    >>> import pandas as pd
    >>> x = pd.DataFrame({"name": ["Mick", "John", "Paul"]})
    >>> y = pd.DataFrame(
    ...     {"name": ["John", "Paul"], "plays": ["guitar", "bass"]}
    ... )
    >>> inner_join(x, y, by="name")["name"].tolist()
    ['John', 'Paul']
    """
    by = _validate_join_args(x, y, by)
    # Add positional index to preserve x row order after merge
    x_idx = x.assign(**{"._x_idx": range(len(x))})
    out = pd.merge(x_idx, y, on=by, how="inner", sort=False)
    out = out.sort_values("._x_idx").drop(columns=["._x_idx"]).reset_index(drop=True)
    return out


def left_join(
    x: pd.DataFrame,
    y: pd.DataFrame,
    by: str | list[str],
) -> pd.DataFrame:
    """Left join: return all rows from x, matching rows from y.

    Guarantees exactly ``len(x)`` output rows by tracking x row positions
    through the merge — matches R's index-based reconstruction.

    Parameters
    ----------
    x : pd.DataFrame
        Left DataFrame; every row is kept.
    y : pd.DataFrame
        Right DataFrame.
    by : str or list of str
        Column name(s) to join on. Must exist in both ``x`` and ``y`` with
        matching dtypes.

    Returns
    -------
    pd.DataFrame
        All rows from ``x``, with matching columns from ``y`` where
        available (``NaN`` otherwise).

    Examples
    --------
    >>> import pandas as pd
    >>> x = pd.DataFrame({"name": ["Mick", "John", "Paul"]})
    >>> y = pd.DataFrame(
    ...     {"name": ["John", "Paul"], "plays": ["guitar", "bass"]}
    ... )
    >>> left_join(x, y, by="name")["name"].tolist()
    ['Mick', 'John', 'Paul']
    """
    by_list = _validate_join_args(
        x,
        y,
        by,
        require_x_unique=True,
        require_y_unique=True,
        require_x_complete=False,  # R allows NA keys in x for left join
        require_y_complete=True,
    )
    # Attach a positional index to reconstruct exact x row order/count
    x_idx = x.assign(**{"._x_idx": range(len(x))})
    out = pd.merge(x_idx, y, on=by_list, how="left", sort=False)
    # Re-sort by the original x position and take exactly len(x) rows
    out = out.sort_values("._x_idx").drop(columns=["._x_idx"]).iloc[: len(x)].reset_index(drop=True)
    return out


def right_join(
    x: pd.DataFrame,
    y: pd.DataFrame,
    by: str | list[str],
) -> pd.DataFrame:
    """Right join: equivalent to left_join(y, x, by).

    Parameters
    ----------
    x : pd.DataFrame
        Left DataFrame.
    y : pd.DataFrame
        Right DataFrame; every row is kept.
    by : str or list of str
        Column name(s) to join on. Must exist in both ``x`` and ``y`` with
        matching dtypes.

    Returns
    -------
    pd.DataFrame
        All rows from ``y``, with matching columns from ``x`` where
        available (``NaN`` otherwise).

    Examples
    --------
    >>> import pandas as pd
    >>> x = pd.DataFrame(
    ...     {
    ...         "name": ["Mick", "John", "Paul"],
    ...         "band": ["Stones", "Beatles", "Beatles"],
    ...     }
    ... )
    >>> y = pd.DataFrame({"name": ["John", "Paul", "Keith"]})
    >>> right_join(x, y, by="name")["name"].tolist()
    ['John', 'Paul', 'Keith']
    """
    return left_join(x=y, y=x, by=by)


def full_join(
    x: pd.DataFrame,
    y: pd.DataFrame,
    by: str | list[str],
) -> pd.DataFrame:
    """Full (outer) join: return all rows from both x and y.

    Parameters
    ----------
    x : pd.DataFrame
        Left DataFrame.
    y : pd.DataFrame
        Right DataFrame.
    by : str or list of str
        Column name(s) to join on. Must exist in both ``x`` and ``y`` with
        matching dtypes.

    Returns
    -------
    pd.DataFrame
        Union of rows from ``x`` and ``y``, with ``NaN`` in columns unique
        to the side that didn't match.

    Examples
    --------
    >>> import pandas as pd
    >>> x = pd.DataFrame({"name": ["Mick", "John"]})
    >>> y = pd.DataFrame({"name": ["John", "Keith"]})
    >>> len(full_join(x, y, by="name"))
    3
    """
    by = _validate_join_args(x, y, by)
    out = pd.merge(x, y, on=by, how="outer", sort=False)
    out = out.reset_index(drop=True)
    return out


def semi_join(
    x: pd.DataFrame,
    y: pd.DataFrame,
    by: str | list[str],
) -> pd.DataFrame:
    """Semi join: return rows from x that have matches in y.

    Parameters
    ----------
    x : pd.DataFrame
        Left DataFrame.
    y : pd.DataFrame
        Right DataFrame, used only to test for a match.
    by : str or list of str
        Column name(s) to join on. Must exist in both ``x`` and ``y`` with
        matching dtypes.

    Returns
    -------
    pd.DataFrame
        Rows from ``x`` with a matching key in ``y``, keeping only ``x``'s
        columns.

    Examples
    --------
    >>> import pandas as pd
    >>> x = pd.DataFrame({"name": ["Mick", "John", "Paul"]})
    >>> y = pd.DataFrame(
    ...     {"name": ["John", "Paul"], "plays": ["guitar", "bass"]}
    ... )
    >>> semi_join(x, y, by="name")["name"].tolist()
    ['John', 'Paul']
    """
    by = _validate_join_args(x, y, by)
    # Add positional index to preserve x order
    x_idx = x.assign(**{"._x_idx": range(len(x))})
    merged = pd.merge(x_idx, y[by], on=by, how="inner", sort=False)
    out = (
        pd.DataFrame(merged[["._x_idx", *list(x.columns)]])
        .drop_duplicates(subset=["._x_idx"])
        .sort_values("._x_idx")
        .drop(columns=["._x_idx"])
        .reset_index(drop=True)
    )
    return out


def anti_join(
    x: pd.DataFrame,
    y: pd.DataFrame,
    by: str | list[str],
) -> pd.DataFrame:
    """Anti join: return rows from x that have no match in y.

    Parameters
    ----------
    x : pd.DataFrame
        Left DataFrame.
    y : pd.DataFrame
        Right DataFrame, used only to test for a match.
    by : str or list of str
        Column name(s) to join on. Must exist in both ``x`` and ``y`` with
        matching dtypes.

    Returns
    -------
    pd.DataFrame
        Rows from ``x`` with no matching key in ``y``.

    Examples
    --------
    >>> import pandas as pd
    >>> x = pd.DataFrame({"name": ["Mick", "John", "Paul"]})
    >>> y = pd.DataFrame(
    ...     {"name": ["John", "Paul"], "plays": ["guitar", "bass"]}
    ... )
    >>> anti_join(x, y, by="name")["name"].tolist()
    ['Mick']
    """
    by = _validate_join_args(x, y, by)
    indicator = pd.merge(x, y[by], on=by, how="left", indicator=True, sort=False)
    mask = indicator["_merge"] == "left_only"
    out = x.loc[mask.values].reset_index(drop=True)
    return out
