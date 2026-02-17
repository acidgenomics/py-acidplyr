"""Tests for select_if."""

import numpy as np
import pandas as pd
import pytest

from acidplyr import select_if


@pytest.fixture()
def df():
    return pd.DataFrame(
        {
            "a": [1.0, 2.0, 3.0],
            "b": [4, 5, 6],
            "c": ["x", "y", "z"],
        }
    )


def test_select_float(df):
    result = select_if(df, predicate=lambda col: col.dtype == np.float64)
    assert list(result.columns) == ["a"]


def test_select_numeric(df):
    result = select_if(
        df,
        predicate=lambda col: pd.api.types.is_numeric_dtype(col),
    )
    assert list(result.columns) == ["a", "b"]


def test_no_match(df):
    with pytest.raises(ValueError):
        select_if(df, predicate=lambda col: col.dtype == np.bool_)
