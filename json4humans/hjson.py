"""
HJSON implementation for Python

Specifications are available here : https://hjson.github.io/
"""
from __future__ import annotations

from typing import Any, TextIO, cast

from lark import Lark, Token, v_args
from lark.visitors import merge_transformers

from . import json, json5, wsc
from .env import DEBUG
from .jsonc import JSONCEncoder
from .style import StylePreservingTransformer
from .types import (  # noqa: F401
    WSC,
    Array,
    Float,
    HexInteger,
    Ident,
    Identifier,
    Integer,
    Key,
    Object,
    Quote,
    String,
    Value,
)

Member = tuple[Key, Value]


class HJSONTransformer(StylePreservingTransformer):
    @v_args(inline=True)
    def string(self, s):
        return s

    def object_with_trailing(self, children: list) -> Any:
        o = Object(cast(Member, c) for c in children if isinstance(c, tuple))
        o.json_container_tail = children[-2]
        o.json_container_trailing_coma = isinstance(children[-3], Token)
        return o


transformer = merge_transformers(
    HJSONTransformer(), json=json.transformer, json5=json5.transformer, wsc=wsc.transformer
)


class HJSONEncoder(JSONCEncoder):
    pass


_params = dict(
    parser="lalr",
    start="value",
    maybe_placeholders=True,
    regex=True,
)

if not DEBUG:
    _params["transformer"] = transformer

parser = Lark.open("grammar/hjson.lark", rel_to=__file__, **_params)


def loads(src: str) -> Any:
    if DEBUG:
        tree = parser.parse(src)
        return transformer.transform(tree)
    else:
        return parser.parse(src)


def load(file: TextIO) -> str:
    return loads(file.read())


def dumps(obj: Any) -> str:
    return HJSONEncoder().encode(obj)


def dump(obj: Any, out: TextIO):
    out.write(dumps(obj))
    out.write("\n")
