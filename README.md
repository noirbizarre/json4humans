# json4humans

[![CI](https://github.com/noirbizarre/json4humans/actions/workflows/ci.yml/badge.svg)](https://github.com/noirbizarre/json4humans/actions/workflows/ci.yml)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/noirbizarre/json4humans/main.svg)](https://results.pre-commit.ci/latest/github/noirbizarre/json4humans/main)
[![Maintainability](https://api.codeclimate.com/v1/badges/54c04851ef133974e718/maintainability)](https://codeclimate.com/github/noirbizarre/json4humans/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/54c04851ef133974e718/test_coverage)](https://codeclimate.com/github/noirbizarre/json4humans/test_coverage)

Python tools for JSONC and JSON5 (aka. JSON for humans)

This package provider parsing and serialization (with style preservation)
as well as linting, formatting and cli tools for [JSON](https://www.json.org/)-derived syntaxes.

## Supported formats

While all thise started with JSONC support, it quickly moved to also support `JSON5` then other derivated.
As of today, JSON4Humans support the following formats:

- [JSON](./#JSON)
- [JSONC](./#JSON-with-comments-JSONC)
- [JSON5](./#JSON5)


### JSON

While [JSON](https://www.json.org/) is natively supported by Python standard library,
the builtin module doesn't provide style preservation.
The one provided by `json4humans` do.

### JSON with comments (JSONC)

This is a format introduced by [github/Microsoft in VSCode](https://code.visualstudio.com/docs/languages/json#_json-with-comments).
This is basically standard JSON with both line and block comments supports as well as optionnal trailing coma support.

### JSON5

[JSON5](https://json5.org/) could be the next real JSON specifications given it has [real specifications](https://specs.json5.org).
In fact I doubt that because if it's a good human readable/editable format (support comments, multilines and a lot of other syntaxes sugars)
it's not a good machine-readable format anymore. Anyway, it's an interesting format into which style/format is important.

## Why ?

### Why a new library ? Why a all-in-on library ?

I've often been strugling with those file-format edition with style preservation.
This is a reccurrent problem (this has all started with JSONC edition in [PDM-VSCode](https://github.com/noirbizarre/pdm-vscode)).

Each time I work with a format, I want to be able to edit-it with style preservation (aka. rount-trip support)
but I also often want to:

- lint-it
- format-it easily
- query-it like I do with JSON and `jq`
- object-like access when possible (like it's done in JavaScript)

Those use cases are the targeted shared features for all supported formats.

## Why only those formats ?

Those are the format I needed to handle but given this library provides a common architecture for all formats
I am totally open to add extra format that can be integated inthis library.

Given I need those use cases for every file format I use,
I don't exclude futures supports for other file formats like:

- [HJSON](https://hjson.github.io/)
- [JSON6](https://github.com/d3x0r/JSON6)
- [JSOX](https://github.com/d3x0r/JSOX)
- [JSON Lines (JSONL)](https://jsonlines.org/)
- [TOML](https://toml.io/)
- [YAML](https://yaml.org/)
- [StrictYAML](https://hitchdev.com/strictyaml/)

### Why this name ?

The name JSON4Humans comes from the recurrent tagline of those formats specifications and libs.
As exemple, from the official pages for JSON5 and HJSon, thei tagline is:

- JSON5: JSON for Humans
- HJson: a user interface for JSON and later in the documentation "It's H for Human, Human JSON."
