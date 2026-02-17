"""Tests for melt."""

import numpy as np
import pandas as pd
import pytest

from acidplyr import melt


@pytest.fixture()
def mat():
    """4x4 integer matrix as DataFrame."""
    data = np.arange(1, 17).reshape(4, 4)
    return pd.DataFrame(
        data,
        index=[f"gene{i}" for i in range(1, 5)],
        columns=[f"sample{i}" for i in range(1, 5)],
    )


def test_default(mat):
    result = melt(mat)
    assert result.shape == (16, 3)
    assert list(result.columns) == ["rowname", "colname", "value"]


def test_colnames(mat):
    result = melt(mat, colnames=["sample1", "sample2"])
    assert result.shape == (8, 3)


def test_min_absolute(mat):
    result = melt(mat, min=5, min_method="absolute")
    assert (result["value"] >= 5).all()


def test_min_per_row(mat):
    result = melt(mat, min=2, min_method="perRow")
    assert len(result) > 0


def test_trans_log2(mat):
    result = melt(mat, trans="log2")
    # log2(1 + 1) = 1.0 (minimum value is 1, transform is log2(x+1))
    expected = np.log2(1 + 1)
    assert np.isclose(result["value"].min(), expected, atol=1e-10)


def test_trans_log10(mat):
    result = melt(mat, trans="log10")
    # log10(1 + 1) = ~0.301 (minimum value is 1, transform is log10(x+1))
    expected = np.log10(1 + 1)
    assert np.isclose(result["value"].min(), expected, atol=1e-10)


def test_lacking_names():
    data = np.array([[1, 2], [3, 4]])
    df = pd.DataFrame(data)
    result = melt(df)
    assert result.shape == (4, 3)


def test_invalid_trans(mat):
    with pytest.raises(ValueError):
        melt(mat, trans="log3")
