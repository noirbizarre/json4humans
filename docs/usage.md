# Getting started

## Installation

Install `json4humans` as you would for any other Python package.

```shell
# with pip
$ pip install json4humans
# with pipenv
$ pipenv install json4humans
#with  PDM
$ pdm add json4humans
```

## TL;DR

All JSON4Humans modules implements the [JSON Module protocol][json4humans.protocol.JSONModule]
and so behave exactly like the [Python builtin json module][json].
Just import the desired syntax module and use it as you would with the builtin moodule.

=== "JSON"

    ```python
    --8<-- "json/basic.py"
    ```

=== "JSONC"

    ```python
    --8<-- "jsonc/basic.py"
    ```

=== "JSON5"

    ```python
    --8<-- "json5/basic.py"
    ```

## The JSON Module protocol

All supported formats modules implements the [JSON Module protocol][json4humans.protocol.JSONModule]
which is trying to mimic as much as possible the [Python builtin json module][json].

```python
--8<-- "jsonmodule.py"
```

