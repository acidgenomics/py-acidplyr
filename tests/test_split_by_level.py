"""Tests for split_by_level."""

import pandas as pd
import pytest

from acidplyr import split_by_level


@pytest.fixture
def df():
    return pd.DataFrame(
        {
            "compound": pd.Categorical(
                ["aspirin", "aspirin", "ibuprofen", "ibuprofen"],
                categories=["aspirin", "ibuprofen"],
            ),
            "concentration": pd.Categorical(
                ["low", "high", "low", "high"],
                categories=["low", "high"],
            ),
            "value": [1, 2, 3, 4],
        }
    )


def test_split_compound(df):
    result = split_by_level(df, f="compound")
    assert len(result) == 2
    assert "aspirin" in result
    assert len(result["aspirin"]) == 2


def test_split_concentration(df):
    result = split_by_level(df, f="concentration")
    assert len(result) == 2
    assert len(result["low"]) == 2


def test_split_with_ref(df):
    result = split_by_level(df, f="compound", ref=True)
    assert len(result) == 2
    assert len(result["aspirin"]) == 2
    assert len(result["ibuprofen"]) == 4


def test_non_categorical():
    df = pd.DataFrame({"a": ["x", "y"], "b": [1, 2]})
    with pytest.raises(TypeError):
        split_by_level(df, f="a")


def test_missing_column():
    df = pd.DataFrame({"a": pd.Categorical(["x", "y"])})
    with pytest.raises(KeyError):
        split_by_level(df, f="z")
