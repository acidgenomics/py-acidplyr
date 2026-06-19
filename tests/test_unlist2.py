"""Tests for unlist2."""

import pandas as pd
import pytest

from acidplyr import unlist2


def test_everything_named():
    x = {
        "grp1": pd.DataFrame({"a": [1, 2], "b": ["x", "y"]}, index=["r1", "r2"]),
        "grp2": pd.DataFrame({"a": [3, 4], "b": ["z", "w"]}, index=["r3", "r4"]),
    }
    result = unlist2(x)
    assert result.shape == (4, 4)
    assert list(result.columns) == ["name", "rowname", "a", "b"]
    assert list(result["name"]) == ["grp1", "grp1", "grp2", "grp2"]


def test_only_colnames():
    x = {
        "a": pd.DataFrame({"val": [10, 20]}),
        "b": pd.DataFrame({"val": [30, 40]}),
    }
    result = unlist2(x)
    assert result.shape == (4, 3)


def test_empty_dict():
    with pytest.raises(ValueError, match="length 0"):
        unlist2({})


def test_non_dataframe_element():
    x = {"a": [1, 2, 3]}
    with pytest.raises(TypeError):
        unlist2(x)
