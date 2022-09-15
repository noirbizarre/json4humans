"""
This modules provides some helpers to handle style preservation.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Generic, TypeAlias, TypeVar, cast

from lark import Token
from lark.visitors import Transformer, v_args

from . import wsc
from .protocol import JSONEncoder
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


Encoder = TypeVar("Encoder", bound=JSONEncoder)
T = TypeVar("T")


JSONEncoderMethod: TypeAlias = Callable[[Encoder, T], str]
"""A JSON encoder type method"""

JSONEncoderBoundMethod: TypeAlias = Callable[[T], str]
"""A JSON encoder bound type method"""


class with_style(Generic[Encoder, T]):
    encoder: Encoder

    def __init__(self, fn: JSONEncoderMethod):
        self.fn = fn

    def __call__(self, obj: T) -> str:
        return "".join(
            (
                "".join(wsc.encode_wsc(w) for w in getattr(obj, "json_before", [])),
                self.fn(self.encoder, obj),
                "".join(wsc.encode_wsc(w) for w in getattr(obj, "json_after", [])),
            )
        )

    def __get__(self, instance, owner) -> JSONEncoderBoundMethod:
        self.encoder = instance
        return self.__call__
