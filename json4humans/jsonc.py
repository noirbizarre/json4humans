"""
This module provides supprot for the `JSONC` file format

This is a format introduced by
[github/Microsoft in VSCode](https://code.visualstudio.com/docs/languages/json#_json-with-comments).
This is basically standard JSON with both line and block comments
supports as well as optionnal trailing coma support.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, TextIO

from lark import Lark
from lark.visitors import merge_transformers

from . import json, wsc
from .env import DEBUG
from .style import StylePreservingTransformer
from .types import WSC, Array, Float, Integer, JSONType, Object, String  # noqa: F401

Member = tuple[String, JSONType]


class JSONCTransformer(StylePreservingTransformer):
    """
    A [Transformer][lark.visitors.Transformer] for JSONC aka. JSON with Comments
    """

    pass


transformer = merge_transformers(JSONCTransformer(), json=json.transformer, wsc=wsc.transformer)


class JSONCEncoder(json.JSONEncoder):
    pass


@dataclass
class FormatOptions:
    trim_whitespaces: bool = False
    remove_comments: bool = False
    keep_newlines: bool = False
    add_end_line_return: bool = True


_params = dict(
    lexer="basic",
    parser="lalr",
    start="value",
    maybe_placeholders=False,
    regex=True,
)

if not DEBUG:
    _params["transformer"] = transformer

parser = Lark.open("grammar/jsonc.lark", rel_to=__file__, **_params)


def loads(src: str) -> Any:
    if DEBUG:
        tree = parser.parse(src)
        return transformer.transform(tree)
    else:
        return parser.parse(src)


def load(file: TextIO) -> str:
    return loads(file.read())


def dumps(obj: Any) -> str:
    return JSONCEncoder().encode(obj)


def dump(obj: Any, out: TextIO):
    out.write(dumps(obj))
    out.write("\n")
