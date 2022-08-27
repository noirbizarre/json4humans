from __future__ import annotations

from enum import Enum
from typing import Any, Generic, Iterable, OrderedDict, Protocol, TextIO, TypeVar, runtime_checkable


@runtime_checkable
class JSONModule(Protocol):
    """
    Protocol for JSON modules implemnentation
    """

    def loads(self, src: str) -> Any:
        ...

    def load(self, file: TextIO) -> Any:
        ...

    def dumps(self, obj: Any) -> str:
        ...

    def dump(self, obj: Any, out: TextIO):
        ...


class JSONType:
    """
    Base class for parsed types with style and metadata preservation.
    """

    json_before: list[WSC]
    json_after: list[WSC]

    def __init__(
        self, *_, before: list[WSC | str] | None = None, after: list[WSC | str] | None = None, **__
    ):
        from . import wsc

        self.json_before = wsc.parse_list(before)
        self.json_after = wsc.parse_list(after)


class Container(JSONType):
    """
    Base class for containers with style and metadata preservation.
    """

    json_container_head: list[WSC]
    json_container_tail: list[WSC]
    json_container_trailing_coma: bool

    def __init__(
        self,
        *args,
        before: list[WSC | str] | None = None,
        after: list[WSC | str] | None = None,
        head: list[WSC | str] | None = None,
        tail: list[WSC | str] | None = None,
        trailing_coma: bool = False,
        **kwargs,
    ):
        super().__init__(*args, before=before, after=after, **kwargs)
        from . import wsc

        self.json_container_head = wsc.parse_list(head)
        self.json_container_tail = wsc.parse_list(tail)
        self.json_container_trailing_coma = trailing_coma


class WhiteSpace(str):
    def __repr__(self) -> str:
        return f"WhiteSpace({super().__repr__()})"


class Comment(str):
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({super().__repr__()})"


WSC = WhiteSpace | Comment


class BlockStyleComment(Comment):
    pass


class LineStyleComment(Comment):
    pass


class HashStyleComment(Comment):
    pass


class Object(OrderedDict, Container):
    pass


class Array(list["Value"], Container):
    def __init__(
        self,
        items: Iterable,
        *,
        before: list[WSC | str] | None = None,
        after: list[WSC | str] | None = None,
        head: list[WSC | str] | None = None,
        tail: list[WSC | str] | None = None,
        trailing_coma: bool = False,
        **kwargs,
    ):
        list.__init__(self, items or [])
        Container.__init__(
            self, before=before, after=after, head=head, tail=tail, trailing_coma=trailing_coma
        )

    def __repr__(self) -> str:
        return f"Array({super().__repr__()})"


class Identifier(str, JSONType):
    def __repr__(self) -> str:
        return f"Identifier({super().__repr__()})"


Ident = Identifier


class Quote(Enum):
    SINGLE = "'"
    DOUBLE = '"'


class String(str, JSONType):
    quote: Quote
    linebreaks: list[int]

    def __new__(cls, value, *args, **kwargs):
        # explicitly only pass value to the str constructor
        return super().__new__(cls, value)

    def __init__(
        self,
        _,
        quote: str | Quote = Quote.DOUBLE,
        linebreaks: list[int] | None = None,
        before: list[WSC | str] | None = None,
        after: list[WSC | str] | None = None,
    ):
        super().__init__(before=before, after=after)
        self.quote = Quote(quote) if isinstance(quote, str) else quote
        self.linebreaks = linebreaks or []

    def __repr__(self) -> str:
        return f"String({super().__repr__()}, quote={self.quote})"


Key = String | Identifier | str


class NumericLiteral(Enum):
    Infinity = float("Inf")
    NaN = float("NaN")


class NumericSign(Enum):
    PLUS = "+"
    MINUS = "-"


class Number(JSONType):
    prefixed: bool

    def __new__(cls, value, *args, **kwargs):
        number = super().__new__(cls, value)
        number.prefixed = kwargs.get("prefixed", False)
        return number

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({super().__repr__()}, prefixed={self.prefixed})"

    def __str__(self) -> str:
        return super().__repr__()


class Integer(Number, int):
    pass


class HexInteger(Integer):
    def __str__(self) -> str:
        return hex(self)


class Float(Number, float):
    leading_point: bool
    significand: int | None

    def __new__(cls, value, *args, **kwargs):
        number = super().__new__(cls, value, prefixed=kwargs.get("prefixed", False))
        number.leading_point = kwargs.get("leading_point", False)
        number.significand = kwargs.get("significand")
        return number

    def __str__(self) -> str:
        raw = super().__str__()
        if self.leading_point and raw.startswith("0"):
            return raw[1:]
        if self.significand is not None:
            pos = raw.index(".") + 1
            raw = raw[: pos + self.significand]
        return raw


AnyNumber = Integer | Float

T = TypeVar("T")


class Literal(JSONType, Generic[T]):
    value: T

    def __init__(self, value: T, **kwargs):
        super().__init__(**kwargs)
        self.value = value

    def __eq__(self, obj: object) -> bool:
        return self.value.__eq__(obj)

    def __hash__(self) -> int:
        return self.value.__hash__()

    def __repr__(self) -> str:
        return f"Literal({self.value})"


Value = Object | Array | String | Number | Literal | bool | None

Member = tuple[Key, Value]


class TupleWithTrailingComa(tuple[T, ...]):
    trailing_coma: bool

    def __new__(cls, items, *args, **kwargs):
        # explicitly only pass value to the tuple constructor
        return super().__new__(cls, items)

    def __init__(self, items: Iterable[T], trailing_coma: bool = False):
        self.trailing_coma = trailing_coma
