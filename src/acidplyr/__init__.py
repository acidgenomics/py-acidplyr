"""AcidPlyr: Acid Genomics DataFrame manipulation utilities.

A pandas-based grammar of data manipulation, providing dplyr-like
operations for pandas DataFrames.
"""

from acidplyr._cast import cast
from acidplyr._collapse_to_string import collapse_to_string
from acidplyr._filter_nested import filter_nested
from acidplyr._join import (
    anti_join,
    full_join,
    inner_join,
    left_join,
    right_join,
    semi_join,
)
from acidplyr._melt import melt
from acidplyr._mutate import (
    mutate_all,
    mutate_at,
    mutate_if,
    transmute_at,
    transmute_if,
)
from acidplyr._rbind_to_dataframe import rbind_to_dataframe
from acidplyr._select import select_if
from acidplyr._split_by_level import split_by_level
from acidplyr._unlist2 import unlist2
from acidplyr._unnest2 import unnest2

__all__ = [
    "anti_join",
    "cast",
    "collapse_to_string",
    "filter_nested",
    "full_join",
    "inner_join",
    "left_join",
    "melt",
    "mutate_all",
    "mutate_at",
    "mutate_if",
    "rbind_to_dataframe",
    "right_join",
    "select_if",
    "semi_join",
    "split_by_level",
    "transmute_at",
    "transmute_if",
    "unlist2",
    "unnest2",
]
