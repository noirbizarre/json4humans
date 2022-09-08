"""
This modules provides some helpers to handle style preservation.
"""

from __future__ import annotations

from typing import Any, Callable, cast

from lark import Token
from lark.visitors import Transformer, v_args

from . import wsc
from .types import WSC, Array, JSONType, Key, Member, Object, TupleWithTrailingComa, Value


class StylePreservingTransformer(Transformer):
    """
    A base [Transformer][lark.visitors.Transformer] with helpers to handle style preservation
    """

    @v_args(inline=True)
    def array(
        self, elements: TupleWithTrailingComa[JSONType], tail: list[WSC | str] | None = None
    ) -> Array:
        return Array(elements, tail=tail, trailing_coma=getattr(elements, "trailing_coma", False))

    @v_args(inline=True)
    def value_list(self, *values) -> TupleWithTrailingComa[JSONType]:
        return TupleWithTrailingComa[JSONType](
            (value for value in values if isinstance(value, JSONType)),
            trailing_coma=isinstance(values[-1], Token),
        )

    @v_args(inline=True)
    def object(
        self, members: TupleWithTrailingComa[Member], tail: list[WSC | str] | None = None, last=None
    ) -> Object:
        o = Object(members)
        o.json_container_tail = wsc.parse_list(tail)
        return o

    @v_args(inline=True)
    def member_list(self, *members) -> TupleWithTrailingComa[Member]:
        return TupleWithTrailingComa[Member](
            (cast(Member, member) for member in members if isinstance(member, tuple)),
            trailing_coma=isinstance(members[-1], Token),
        )

    def member(self, kv: list[Key | Value]) -> Member:
        assert len(kv) == 2
        return (cast(Key, kv[0]), cast(Value, kv[1]))

    @v_args(inline=True)
    def pack_wsc(self, before: list[WSC], value: JSONType, after: list[WSC]) -> JSONType:
        value.json_before = before
        value.json_after = after
        return value

    value = pack_wsc
    key = pack_wsc


JSONEncoderMethod = Callable[[Any, Any], str]


def with_style(fn: JSONEncoderMethod) -> JSONEncoderMethod:
    """
    A decorator providing whitespaces and comments handling for encoders.

    handling before and after the item for type handlers encoders.
    """

    def encode_with_style(self, obj: Any) -> str:
        return "".join(
            (
                "".join(wsc.encode_wsc(w) for w in getattr(obj, "json_before", [])),
                fn(self, obj),
                "".join(wsc.encode_wsc(w) for w in getattr(obj, "json_after", [])),
            )
        )

    return encode_with_style
