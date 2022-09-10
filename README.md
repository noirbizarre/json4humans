# json4humans

[![CI](https://github.com/noirbizarre/json4humans/actions/workflows/ci.yml/badge.svg)](https://github.com/noirbizarre/json4humans/actions/workflows/ci.yml)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/noirbizarre/json4humans/main.svg)](https://results.pre-commit.ci/latest/github/noirbizarre/json4humans/main)
[![Maintainability](https://api.codeclimate.com/v1/badges/54c04851ef133974e718/maintainability)](https://codeclimate.com/github/noirbizarre/json4humans/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/54c04851ef133974e718/test_coverage)](https://codeclimate.com/github/noirbizarre/json4humans/test_coverage)
[![Documentation Status](https://readthedocs.org/projects/json4humans/badge/?version=latest)](https://json4humans.readthedocs.io/en/latest/?badge=latest)
[![PyPI](https://img.shields.io/pypi/v/json4humans)](https://pypi.org/project/json4humans/)
[![PyPI - License](https://img.shields.io/pypi/l/json4humans)](https://pypi.org/project/json4humans/)


<p align="center">
  <img src="https://raw.githubusercontent.com/noirbizarre/json4humans/main/docs/images/logo-with-text.svg" />
</p>

Python tools for JSONC and JSON5 (aka. JSON for humans)

This package provider parsing and serialization (with style preservation)
as well as linting, formatting and cli tools for [JSON](https://www.json.org/)-derived syntaxes.

## Getting started

Add `json4humans` as a dependency to your project:

```shell
# pip
pip install json4humans
# pipenv
pipenv install json4humans
# PDM
pdm add json4humans
```

Then import the proper module and use it like you would with the builtin `json` module:

```python
from pathlib import Path
from json4humans import json

my_file = Path(__file__).parent / "my_file.json"

# Load data
with my_file.open() as f:
    data = json.load(f)

# Edit
data["attr"] = "value"

# Save with style preservation
with my_file.open("w") as out:
    json.dump(out, data)

```

## Features

- [x] Manipulate all supported format with the exact same API. Currently supported:
  - [JSON](./#JSON)
  - [JSONC](./#JSON-with-comments-JSONC)
  - [JSON5](./#JSON5)
- [x] Parsed data supports native types comparison while preserving style
- [x] Support serialization for both native types and provided `JSONType`
- [ ] Supports formatting
- [ ] Supports linting
- [ ] All features availables as a standalone cli
- [ ] Support `jq`-like queries

## Documentation

Documentation is available at <https://json4humans.rtfd.io>

## Contributing

Read the [dedicated contributing guidelines](./CONTRIBUTING.md).
