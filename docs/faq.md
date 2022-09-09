# Frequently asked questions

## Why a new library ? Why a all-in-on library ?

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
I am totally open to add extra format that can be integated in this library.

Given I need those use cases for every file format I use,
I don't exclude futures supports for other file formats like:

- [HJSON](https://hjson.github.io/)
- [JSON6](https://github.com/d3x0r/JSON6)
- [JSOX](https://github.com/d3x0r/JSOX)
- [JSON Lines (JSONL)](https://jsonlines.org/)
- [TOML](https://toml.io/)
- [YAML](https://yaml.org/)
- [StrictYAML](https://hitchdev.com/strictyaml/)

## Why this name ?

The name JSON4Humans comes from the recurrent tagline of those formats specifications and libs.
As exemple, from the official pages for JSON5 and HJSon, thei tagline is:

- JSON5: JSON for Humans
- HJson: a user interface for JSON and later in the documentation "It's H for Human, Human JSON."
