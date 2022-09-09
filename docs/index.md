---
hide:
  - navigation
  - toc
---
# JSON 4 Humans

<p align="center">
  <img src="https://raw.githubusercontent.com/noirbizarre/json4humans/main/docs/images/logo-with-text.svg" />
</p>

Python tools for JSON and derivateds like JSONC and JSON5 (aka. JSON for humans)

This package provider parsing and serialization (with style preservation)
as well as linting, formatting and cli tools for [JSON](https://www.json.org/)-derived syntaxes.

## Features

- [x] Manipulate all supported format with the exact same API. Currently supported:
    - [x] [JSON][json4humans.json]
    - [x] [JSONC][json4humans.jsonc]
    - [x] [JSON5][json4humans.json5]
- [x] Parsed data supports native types comparison while preserving style
- [x] Support serialization for both native types and provided `JSONType`
- [ ] Supports formatting
- [ ] Supports linting
- [ ] All features availables as a standalone cli
- [ ] Support `jq`-like queries
