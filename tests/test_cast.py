"""Tests for cast."""

import pandas as pd
import pytest

from acidplyr import cast


@pytest.fixture
def long_df():
    """Long-form DataFrame similar to AcidTest::DFrame."""
    df = pd.DataFrame(
        {
            "rowname": ["gene1", "gene1", "gene2", "gene2"],
            "colname": pd.Categorical(["sample1", "sample2", "sample1", "sample2"]),
            "value": [1, 2, 3, 4],
        }
    )
    return df


def test_roundtrip(long_df):
    wide = cast(long_df)
    assert wide.shape == (2, 2)
    assert list(wide.columns) == ["sample1", "sample2"]


def test_cast_requires_categorical():
    df = pd.DataFrame(
        {
            "rowname": ["a", "a"],
            "colname": ["x", "y"],
            "value": [1, 2],
        }
    )
    with pytest.raises(TypeError):
        cast(df)


def test_cast_custom_columns():
    df = pd.DataFrame(
        {
            "rn": ["gene1", "gene1", "gene2", "gene2"],
            "cn": pd.Categorical(["s1", "s2", "s1", "s2"]),
            "val": [10, 20, 30, 40],
        }
    )
    wide = cast(df, col_colname="cn", col_value="val")
    assert wide.shape == (2, 2)
    assert list(wide.index) == ["gene1", "gene2"]
