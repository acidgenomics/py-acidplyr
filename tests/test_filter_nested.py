"""Tests for filter_nested."""

import pandas as pd
import pytest

from acidplyr import filter_nested


@pytest.fixture
def df():
    return pd.DataFrame(
        {
            "a": ["foo", "bar", "baz"],
            "b": ["hello", "world", "foo"],
            "c": [1, 2, 3],
        }
    )


def test_case_sensitive(df):
    result = filter_nested(df, pattern="foo")
    assert len(result) == 2


def test_case_insensitive(df):
    result = filter_nested(df, pattern="FOO", ignore_case=True)
    assert len(result) == 2


def test_no_matches(df):
    result = filter_nested(df, pattern="zzz")
    assert len(result) == 0


def test_nested_list_column():
    df = pd.DataFrame(
        {
            "a": ["x", "y"],
            "b": [["foo", "bar"], ["baz", "qux"]],
        }
    )
    result = filter_nested(df, pattern="foo")
    assert len(result) == 1
