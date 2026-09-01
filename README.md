# py-acidplyr

[![Install with Bioconda](https://img.shields.io/badge/install%20with-bioconda-brightgreen.svg)](https://bioconda.github.io/recipes/acidplyr/README.html) ![Lifecycle: maturing](https://img.shields.io/badge/lifecycle-maturing-blue.svg)

A pandas-based grammar for data frame manipulation.

## Installation

### [uv][] method

This is a [Python][] package hosted on [PyPI][] as `acidgenomics-acidplyr`.
The import name is unchanged: `acidplyr`.
We recommend using [uv][] to install.

```sh
uv add acidgenomics-acidplyr
```

Or with [pip][]:

```sh
pip install acidgenomics-acidplyr
```

### [Conda][] method

Configure [Conda][] to use the [Bioconda][] channels.

```sh
# Don't install recipe into base environment.
name='acidplyr'
conda create --name="$name" "$name"
conda activate "$name"
python -c 'import acidplyr'
```

## Links

- [GitHub](https://github.com/acidgenomics/py-acidplyr)

## License

Apache-2.0 — Copyright 2026 Acid Genomics LLC — see [LICENSE](LICENSE).

[bioconda]: https://bioconda.github.io/
[conda]: https://docs.conda.io/
[pip]: https://pip.pypa.io/
[pypi]: https://pypi.org/project/acidgenomics-acidplyr/
[python]: https://www.python.org/
[uv]: https://docs.astral.sh/uv/
