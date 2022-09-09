"""
This module implements the [JSON module protocol][json4humans.types.JSONModule]
for [JSON5](https://json5.org/).

The JSON5 Data Interchange Format ([JSON5](https://json5.org/)) is a superset of [JSON](https://json.org/)
that aims to alleviate some of the limitations of JSON by expanding its syntax to include some productions
from [ECMAScript 5.1](https://www.ecma-international.org/ecma-262/5.1/).

See: [specifications](https://spec.json5.org)

"""
from __future__ import annotations

import re
from typing import Any, TextIO, cast

from lark import Lark, Token
from lark.visitors import merge_transformers, v_args

from . import json, wsc
from .env import DEBUG
from .jsonc import JSONCEncoder
from .style import StylePreservingTransformer, with_style
from .types import (  # noqa: F401
    WSC,
    AnyNumber,
    Array,
    Float,
    HexInteger,
    Ident,
    Identifier,
    Integer,
    JSONType,
    Key,
    Literal,
    Member,
    Number,
    Object,
    Quote,
    String,
    Value,
)


class JSON5Transformer(StylePreservingTransformer):
    """
    A [Transformer][lark.visitors.Transformer] for JSON5
    """

    @v_args(inline=True)
    def string(self, string: String):
        return string

    @v_args(inline=True)
    def SINGLE_QUOTE_CHARS(self, token: Token) -> str:
        return token.value.replace("\\/", "/").encode().decode("unicode_escape", "surrogatepass")

    @v_args(inline=True)
    def DOUBLE_QUOTE_CHARS(self, token: Token) -> tuple[str, list[int]]:
        return token.value.replace("\\/", "/").encode().decode("unicode_escape", "surrogatepass"), [
            m.start() for m in re.finditer("\\\n", token.value)
        ]

    @v_args(inline=True)
    def double_quote_string(self, string: tuple[str, list[int]] | None = None) -> String:
        value, linebreaks = string or ("", [])
        return String(value, quote=Quote.DOUBLE, linebreaks=linebreaks)

    @v_args(inline=True)
    def single_quote_string(self, string: str | None = None) -> String:
        return String(string or "", quote=Quote.SINGLE)

    @v_args(inline=True)
    def identifier(self, string) -> Identifier:
        return Identifier(string)

    @v_args(inline=True)
    def number(self, number: Number):
        return number

    def SIGNED_HEXNUMBER(self, token: Token):
        return HexInteger(int(token.value, base=16), prefixed=token.value.startswith(("+", "-")))

    def SIGNED_NUMBER(self, token: Token):
        prefixed = token.value.startswith(("+", "-"))
        if "." in token.value or "e" in token.value:
            significand = len(token.value.split(".")[1]) if "." in token.value else None
            return Float(
                token.value,
                prefixed=prefixed,
                leading_point=token.value.startswith("."),
                significand=significand,
            )
        else:
            return Integer(token.value, prefixed=prefixed)

    def object_with_trailing(self, children: list) -> Any:
        o = Object(cast(Member, c) for c in children if isinstance(c, tuple))
        o.json_container_tail = children[-2]
        o.json_container_trailing_coma = isinstance(children[-3], Token)
        return o

    pair = tuple


transformer = merge_transformers(JSON5Transformer(), wsc=wsc.transformer, json=json.transformer)


ESCAPES = {
    "\\": r"\\",
    "\n": r"\n",
    "\r": r"\r",
    "\b": r"\b",
    "\f": r"\f",
    "\t": r"\t",
    "\v": r"\v",
    "\0": r"\0",
    "\u2028": r"\\u2028",
    "\u2029": r"\\u2029",
}


def escape_string(string: str, **escapes: str | int | None) -> str:
    out = string.translate(str.maketrans({**escapes, **ESCAPES}))
    if isinstance(string, String):
        for linebreak in string.linebreaks:
            out = out[: linebreak - 1] + "\\\n" + out[linebreak - 1 :]
    return out


class JSON5Encoder(JSONCEncoder):
    def encode(self, obj: Any) -> str:
        match obj:
            case Number():
                return self.encode_number(obj)
        return super().encode(obj)

    @with_style
    def encode_number(self, obj: AnyNumber) -> str:
        return f"+{obj}" if obj > 0 and obj.prefixed else str(obj)

    @with_style
    def encode_string(self, obj: str) -> str:
        match obj:
            case String():
                return f"{obj.quote.value}{escape_string(obj)}{obj.quote.value}"
            case Identifier():
                return str(obj)
        return f'"{escape_string(obj)}"'


_params = dict(
    parser="lalr",
    start="value",
    maybe_placeholders=False,
    regex=True,
)

if not DEBUG:
    _params["transformer"] = transformer

parser = Lark.open("grammar/json5.lark", rel_to=__file__, **_params)


def loads(src: str) -> Any:
    if DEBUG:
        tree = parser.parse(src)
        return transformer.transform(tree)
    else:
        return parser.parse(src)


def load(file: TextIO) -> str:
    return loads(file.read())


def dumps(obj: Any) -> str:
    return JSON5Encoder().encode(obj)


def dump(obj: Any, out: TextIO):
    out.write(dumps(obj))
    out.write("\n")
