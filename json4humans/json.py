"""
This module implements the [JSONModule protocol][json4humans.types.JSONModule]
for [JSON](https://www.json.org/).

While [JSON](https://www.json.org/) is natively supported by Python standard library,
the builtin module doesn't provide style preservation.

This one do by returning [style preserving types][json4humans.types] storing whitespaces.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, TextIO

from lark import Lark, Token
from lark.visitors import merge_transformers, v_args

from . import wsc
from .env import DEBUG
from .style import StylePreservingTransformer, with_style
from .types import (  # noqa: F401
    WSC,
    Array,
    Container,
    Float,
    Integer,
    JSONType,
    Literal,
    Member,
    Number,
    Object,
    String,
)


class JSONTransformer(StylePreservingTransformer):
    """
    A [Transformer][lark.visitors.Transformer] for JSON
    """

    @v_args(inline=True)
    def string(self, s):
        return String(
            s[1:-1].replace("\\/", "/").encode().decode("unicode_escape", "surrogatepass")
        )

    @v_args(inline=True)
    def number(self, num: str):
        return Float(num) if "." in num or "e" in num else Integer(num)

    @v_args(inline=True)
    def literal(self, token: Token) -> Literal:
        match token.value:
            case "true":
                return Literal[bool](True)
            case "false":
                return Literal[bool](False)
            case "null":
                return Literal[None](None)
        raise ValueError(f"Unknown literal: {token.value}")


transformer = merge_transformers(JSONTransformer(), wsc=wsc.transformer)


class JSONEncoder:
    """
    The default JSON Encoder
    """

    def encode(self, obj: Any) -> str:
        match obj:
            case bool():
                return self.encode_bool(obj)
            case str():
                return self.encode_string(obj)
            case int():
                return self.encode_int(obj)
            case float():
                return self.encode_float(obj)
            case dict():
                return self.encode_dict(obj)
            case list() | tuple():
                return self.encode_iterable(obj)
            case Literal():
                return self.encode_literal(obj)
        raise NotImplementedError(f"Unknown type: {type(obj)}")

    @with_style
    def encode_string(self, obj: str) -> str:
        return f'"{obj}"'

    @with_style
    def encode_int(self, obj: int) -> str:
        return str(obj)

    @with_style
    def encode_float(self, obj: float) -> str:
        return str(obj)

    @with_style
    def encode_bool(self, obj: bool) -> str:
        return "true" if obj else "false"

    @with_style
    def encode_literal(self, obj: Literal) -> str:
        match obj.value:
            case True:
                return "true"
            case False:
                return "false"
            case None:
                return "null"
        raise NotImplementedError(f"Unknown literal: {obj.value}")

    @with_style
    def encode_dict(self, obj: dict) -> str:
        return "".join(
            (
                "{",
                "".join(wsc.encode_wsc(w) for w in getattr(obj, "json_container_head", [])),
                ",".join(self.encode_pair(k, v) for k, v in obj.items()),
                "," if getattr(obj, "json_container_trailing_coma", False) else "",
                "".join(wsc.encode_wsc(w) for w in getattr(obj, "json_container_tail", [])),
                "}",
            )
        )

    @with_style
    def encode_iterable(self, obj: list | tuple) -> str:
        return "".join(
            (
                "[",
                "".join(wsc.encode_wsc(w) for w in getattr(obj, "json_container_head", [])),
                ",".join(self.encode(item) for item in obj),
                "," if getattr(obj, "json_container_trailing_coma", False) else "",
                "".join(wsc.encode_wsc(w) for w in getattr(obj, "json_container_tail", [])),
                "]",
            )
        )

    def encode_pair(self, key: str, value: Any) -> str:
        return f"{self.encode(key)}:{self.encode(value)}"


@dataclass
class FormatOptions:
    trim_whitespaces: bool = False
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

parser = Lark.open("grammar/json.lark", rel_to=__file__, **_params)


def loads(src: str) -> Any:
    """
    Parse JSON from a string
    """
    if DEBUG:
        tree = parser.parse(src)
        return transformer.transform(tree)
    else:
        return parser.parse(src)


def load(file: TextIO) -> str:
    """
    Parse JSON from a file-like object
    """
    return loads(file.read())


def dumps(obj: Any) -> str:
    """
    Serialize JSON to a string
    """
    return JSONEncoder().encode(obj)


def dump(obj: Any, out: TextIO):
    """
    Serialize JSON to a file-like object
    """
    out.write(dumps(obj))
    out.write("\n")
