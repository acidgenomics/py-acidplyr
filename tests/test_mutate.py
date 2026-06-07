"""Tests for mutate and transmute functions."""

import numpy as np
import pandas as pd
import pytest

from acidplyr import (
    mutate_all,
    mutate_at,
    mutate_if,
    transmute_at,
    transmute_if,
)

EXPECTED_2 = 2.0
EXPECTED_4 = 4.0
EXPECTED_8 = 8.0
EXPECTED_10 = 10.0
EXPECTED_101 = 101.0


@pytest.fixture
def df():
    return pd.DataFrame(
        {
            "a": [1.0, 2.0, 3.0],
            "b": [4.0, 5.0, 6.0],
            "c": ["x", "y", "z"],
        }
    )


def test_mutate_all():
    df = pd.DataFrame({"a": [1.0, 2.0], "b": [3.0, 4.0]})
    result = mutate_all(df, fun=lambda x: x * 2)
    assert result["a"].iloc[0] == EXPECTED_2
    assert result["b"].iloc[1] == EXPECTED_8


def test_mutate_at(df):
    result = mutate_at(df, vars=["a", "b"], fun=lambda x: x * 10)
    assert result["a"].iloc[0] == EXPECTED_10
    assert result["c"].iloc[0] == "x"


def test_mutate_if(df):
    result = mutate_if(
        df,
        predicate=lambda col: col.dtype == np.float64,
        fun=lambda x: x + 100,
    )
    assert result["a"].iloc[0] == EXPECTED_101
    assert result["c"].iloc[0] == "x"


def test_transmute_at(df):
    result = transmute_at(df, vars=["a"], fun=lambda x: x**2)
    assert list(result.columns) == ["a"]
    assert result["a"].iloc[1] == EXPECTED_4


def test_transmute_if(df):
    result = transmute_if(
        df,
        predicate=lambda col: col.dtype == np.float64,
        fun=lambda x: x - 1,
    )
    assert "c" not in result.columns
    assert result["a"].iloc[0] == 0.0
