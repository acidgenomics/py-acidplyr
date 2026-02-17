"""Tests for join functions."""

import pandas as pd
import pytest

from acidplyr import (
    anti_join,
    full_join,
    inner_join,
    left_join,
    right_join,
    semi_join,
)


@pytest.fixture()
def members():
    return pd.DataFrame(
        {
            "name": ["Mick", "John", "Paul"],
            "band": ["Stones", "Beatles", "Beatles"],
        }
    )


@pytest.fixture()
def instruments():
    return pd.DataFrame(
        {
            "name": ["John", "Paul", "Keith"],
            "plays": ["guitar", "bass", "guitar"],
        }
    )


def test_inner_join(members, instruments):
    result = inner_join(members, instruments, by="name")
    assert len(result) == 2
    assert set(result["name"]) == {"John", "Paul"}


def test_left_join(members, instruments):
    result = left_join(members, instruments, by="name")
    assert len(result) == 3
    assert result["plays"].isna().sum() == 1


def test_right_join(members, instruments):
    result = right_join(members, instruments, by="name")
    assert len(result) == 3
    assert result["band"].isna().sum() == 1


def test_full_join(members, instruments):
    result = full_join(members, instruments, by="name")
    assert len(result) == 4


def test_semi_join(members, instruments):
    result = semi_join(members, instruments, by="name")
    assert len(result) == 2
    assert "plays" not in result.columns


def test_anti_join(members, instruments):
    result = anti_join(members, instruments, by="name")
    assert len(result) == 1
    assert result["name"].iloc[0] == "Mick"


def test_inner_join_matched():
    x = pd.DataFrame({"a": [1, 2, 3], "b": ["x", "y", "z"]})
    y = pd.DataFrame({"a": [1, 2, 3], "c": ["p", "q", "r"]})
    result = inner_join(x, y, by="a")
    assert result.shape == (3, 3)


def test_inner_join_unmatched():
    x = pd.DataFrame({"a": [1, 2], "b": ["x", "y"]})
    y = pd.DataFrame({"a": [3, 4], "c": ["p", "q"]})
    result = inner_join(x, y, by="a")
    assert len(result) == 0


def test_left_join_with_duplicates():
    x = pd.DataFrame({"a": [1, 1, 2], "b": ["x", "y", "z"]})
    y = pd.DataFrame({"a": [1, 2], "c": ["p", "q"]})
    result = left_join(x, y, by="a")
    assert len(result) == 3


def test_join_by_multiple():
    x = pd.DataFrame({"a": [1, 2], "b": ["x", "y"], "val": [10, 20]})
    y = pd.DataFrame({"a": [1, 2], "b": ["x", "z"], "val2": [30, 40]})
    result = inner_join(x, y, by=["a", "b"])
    assert len(result) == 1


def test_join_preserves_row_order():
    x = pd.DataFrame({"a": [3, 1, 2], "b": ["c", "a", "b"]})
    y = pd.DataFrame({"a": [1, 2, 3], "c": ["x", "y", "z"]})
    result = left_join(x, y, by="a")
    assert list(result["a"]) == [3, 1, 2]
