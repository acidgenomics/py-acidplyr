"""Tests for collapse_to_string."""

import pandas as pd

from acidplyr import collapse_to_string


def test_atomic_vector():
    result = collapse_to_string(["a", "b", "c"])
    assert result == "a, b, c"


def test_custom_sep():
    result = collapse_to_string(["a", "b", "c"], sep="; ")
    assert result == "a; b; c"


def test_sort():
    result = collapse_to_string(["c", "a", "b"], sort=True)
    assert result == "a, b, c"


def test_unique():
    result = collapse_to_string(["a", "b", "a"], unique=True)
    assert result == "a, b"


def test_na_handling():
    """NA/None values are preserved as 'NA' (R semantics, not stripped)."""
    result = collapse_to_string(["a", None, "b"])
    assert result == "a, NA, b"


def test_scalar():
    result = collapse_to_string("hello")
    assert result == "hello"


def test_dataframe():
    df = pd.DataFrame(
        {
            "a": ["x", "y"],
            "b": [1, 2],
        }
    )
    result = collapse_to_string(df)
    assert isinstance(result, pd.DataFrame)
    assert result.shape == (1, 2)
    assert result["a"].iloc[0] == "x, y"
    assert result["b"].iloc[0] == "1, 2"


def test_numeric_vector():
    result = collapse_to_string([1, 2, 3])
    assert result == "1, 2, 3"
