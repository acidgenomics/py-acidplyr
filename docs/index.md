# acidplyr

A pandas-based grammar for data frame manipulation.

The package provides [dplyr](https://dplyr.tidyverse.org/)-like verbs for pandas
`DataFrame` objects: joins with strict key validation, column-wise mutate/transmute,
and reshape/list utilities for working with nested or wide-format data.

## Installation

### uv method

This package is hosted at [python.acidgenomics.com](https://python.acidgenomics.com/).
We recommend using [uv](https://docs.astral.sh/uv/) to install.

```sh
uv pip install \
    --index-url 'https://python.acidgenomics.com/simple/' \
    acidplyr
```

Or add the index to your project's `pyproject.toml`:

```toml
[[tool.uv.index]]
url = "https://python.acidgenomics.com/simple/"
```

Then install:

```sh
uv add acidplyr
```

### Conda method

Configure [Conda](https://docs.conda.io/) to use the
[Bioconda](https://bioconda.github.io/) channels.

```sh
# Don't install recipe into base environment.
name='acidplyr'
conda create --name="$name" "$name"
conda activate "$name"
python -c 'import acidplyr'
```

## Join operations

Unlike `pandas.merge`, these joins validate that the `by` columns exist in both
frames, have matching dtypes, and (for `inner_join`/`left_join`/etc.) that keys are
unique and complete where required — silent merge mistakes fail loudly instead.

```pycon
>>> import pandas as pd
>>> from acidplyr import inner_join, left_join
>>> members = pd.DataFrame({"name": ["Mick", "John", "Paul"], "band": ["Stones", "Beatles", "Beatles"]})
>>> instruments = pd.DataFrame(
...     {"name": ["John", "Paul", "Keith"], "plays": ["guitar", "bass", "guitar"]}
... )
>>> inner_join(members, instruments, by="name")["name"].tolist()
['John', 'Paul']
>>> left_join(members, instruments, by="name")["name"].tolist()
['Mick', 'John', 'Paul']
```

`right_join`, `full_join`, `semi_join`, and `anti_join` round out the set.

## Mutate and select

`mutate_all`/`mutate_at`/`mutate_if` apply a function across columns and keep the
full frame; the `transmute_*` variants return only the transformed columns.
`select_if` picks columns by predicate.

```pycon
>>> from acidplyr import mutate_at, select_if
>>> df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
>>> mutate_at(df, ["a"], lambda s: s * 2).to_dict("list")
{'a': [2, 4], 'b': [3, 4]}
>>> select_if(df, lambda s: s.sum() > 5).columns.tolist()
['b']
```

## Reshape

`melt` unpivots a wide matrix or `DataFrame` to long format; `cast` reverses it.

```pycon
>>> from acidplyr import melt
>>> import numpy as np
>>> mat = np.array([[1, 2], [3, 4]])
>>> melt(mat).shape
(4, 3)
```

## List and nested data

`unlist2` and `rbind_to_dataframe` flatten dictionaries into a single `DataFrame`;
`unnest2` explodes list-columns; `split_by_level` splits a frame by a categorical
column's levels; `filter_nested` and `collapse_to_string` search and collapse
across nested/list values.

```pycon
>>> from acidplyr import unlist2
>>> d = {"a": pd.DataFrame({"x": [1, 2]}), "b": pd.DataFrame({"x": [3]})}
>>> unlist2(d).to_dict("list")
{'name': ['a', 'a', 'b'], 'rowname': ['0', '1', '0'], 'x': [1, 2, 3]}
```

```{toctree}
:maxdepth: 1
:caption: Contents
:hidden:

reference/index
changelog
```
