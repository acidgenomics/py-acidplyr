"""Tests for unnest2."""

import pandas as pd
import pytest

from acidplyr import unnest2


def test_list_column():
    df = pd.DataFrame(
        {
            "a": ["x", "y"],
            "b": [[1, 2, 3], [4, 5]],
        }
    )
    result = unnest2(df, col="b")
    assert len(result) == 5
    assert list(result.columns) == ["a", "b"]


def test_second_list_column():
    df = pd.DataFrame(
        {
            "id": [1, 2],
            "tags": [["a", "b"], ["c"]],
        }
    )
    result = unnest2(df, col="tags")
    assert len(result) == 3


def test_non_list_column():
    df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
    with pytest.raises(TypeError):
        unnest2(df, col="b")


def test_missing_column():
    df = pd.DataFrame({"a": [1, 2]})
    with pytest.raises(KeyError):
        unnest2(df, col="z")


def test_tuple_column():
    df = pd.DataFrame(
        {
            "a": ["x", "y"],
            "b": [(1, 2), (3, 4, 5)],
        }
    )
    result = unnest2(df, col="b")
    assert len(result) == 5
