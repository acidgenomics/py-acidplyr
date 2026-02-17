"""Cast a long-format DataFrame to wide format."""

import pandas as pd


def cast(
    df: pd.DataFrame,
    col_colname: str = "colname",
    col_value: str = "value",
) -> pd.DataFrame:
    """Cast (pivot) a long-format DataFrame to wide format.

    Parameters
    ----------
    df : pd.DataFrame
        A long-format DataFrame, typically produced by :func:`melt`.
    col_colname : str
        Name of the column containing the column names in long format.
        Must be a categorical (unordered) column.
    col_value : str
        Name of the column containing the values in long format.

    Returns
    -------
    pd.DataFrame
        A wide-format DataFrame.
    """
    if col_colname not in df.columns:
        raise ValueError(f"Column '{col_colname}' not found in DataFrame.")
    if col_value not in df.columns:
        raise ValueError(f"Column '{col_value}' not found in DataFrame.")
    col_data = df[col_colname]
    if not hasattr(col_data, "cat"):
        raise TypeError(
            f"Column '{col_colname}' must be categorical (unordered)."
        )
    if col_data.cat.ordered:
        raise TypeError(f"Column '{col_colname}' must not be ordered.")
    value_data = df[col_value]
    if hasattr(value_data, "cat"):
        raise TypeError(f"Column '{col_value}' must not be categorical.")
    extra_cols = [c for c in df.columns if c not in (col_colname, col_value)]
    categories = list(col_data.cat.categories)
    first_cat = categories[0]
    first_mask = col_data == first_cat
    groups = {}
    for cat in categories:
        mask = col_data == cat
        groups[cat] = value_data[mask].values
    wide = pd.DataFrame(groups)
    if extra_cols:
        row_labels = df.loc[first_mask, extra_cols].reset_index(drop=True)
        if len(extra_cols) == 1:
            wide.index = row_labels.iloc[:, 0].values
        else:
            for ec in extra_cols:
                wide[ec] = row_labels[ec].values
    return wide
