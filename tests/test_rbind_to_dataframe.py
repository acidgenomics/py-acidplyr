"""Tests for rbind_to_dataframe."""

import pytest

from acidplyr import rbind_to_dataframe


def test_matched():
    x = {
        "a": {"col1": 1, "col2": "x"},
        "b": {"col1": 2, "col2": "y"},
    }
    result = rbind_to_dataframe(x)
    assert result.shape == (2, 2)
    assert list(result.index) == ["a", "b"]


def test_unmatched():
    x = {
        "a": {"col1": 1, "col2": "x"},
        "b": {"col1": 2, "col3": "z"},
    }
    result = rbind_to_dataframe(x)
    assert result.shape == (2, 3)


def test_nested_list():
    x = {
        "a": {"col1": 1, "col2": [1, 2, 3]},
        "b": {"col1": 2, "col2": [4, 5, 6]},
    }
    result = rbind_to_dataframe(x)
    assert result.shape == (2, 2)
    assert isinstance(result["col2"].iloc[0], list)


def test_rejects_non_dict():
    with pytest.raises(TypeError):
        rbind_to_dataframe([1, 2, 3])


def test_rejects_empty():
    with pytest.raises(ValueError, match="length 0"):
        rbind_to_dataframe({})
