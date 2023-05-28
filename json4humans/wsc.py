"""
This module handles whitespaces and comments
"""

from __future__ import annotations

from typing import cast

from lark import Lark, Token
from lark.visitors import Transformer, v_args

from .env import DEBUG
from .types import WSC, BlockStyleComment, HashStyleComment, LineStyleComment, WhiteSpace


def parse(wsc: str) -> list[WSC]:
    """
    Parse a string into a list of [WSC][json4humans.types.WSC].

    :param wsc: A string representing whitespaces and/or comments.
    :returns: A list of [WSC][json4humans.types.WSC] only.
    """
    if DEBUG:
        tree = parser.parse(wsc)
        return cast(list[WSC], transformer.transform(tree))
    else:
        return cast(list[WSC], parser.parse(wsc))


def parse_list(items: list[WSC | str] | None = None) -> list[WSC]:
    """
    Parse an optional sequence of whitespaces and comments as [WSC][json4humans.types.WSC] or [str][]
    into a list of [WSC][json4humans.types.WSC] only.

    :param items: An optional list of [WSC][json4humans.types.WSC] or string to be parsed as WSC.
    :returns: A list of [WSC][json4humans.types.WSC].
    """
    if items is None:
        return []
    wscs: list[WSC] = []
    for item in items:
        if isinstance(item, str):
            wscs.extend(parse(item))
        else:
            wscs.append(item)
    return wscs


class WSCTransformer(Transformer):
    """
    A [Transformer][lark.visitors.Transformer] handling whitespaces and comments.
    """

    @v_args(inline=True)
    def WS(self, token: Token) -> WhiteSpace:
        return WhiteSpace(token.value)

    def CPP_COMMENT(self, token: Token) -> LineStyleComment:
        return LineStyleComment(token.value[2:])

    def C_COMMENT(self, token: Token) -> BlockStyleComment:
        return BlockStyleComment(token.value[2:-2])

    def SH_COMMENT(self, token: Token) -> HashStyleComment:
        return HashStyleComment(token.value[1:])

    def wschs(self, wscs: list[WSC]) -> list[WSC]:
        return wscs

    def wscs(self, wscs: list[WSC]) -> list[WSC]:
        return wscs

    def ws(self, wscs: list[WSC]) -> list[WSC]:
        return wscs


transformer = WSCTransformer()


def encode_wsc(wsc: WSC):
    """
    Encode a [WSC][json4humans.types.WSC] into its string representation.

    :param wsc: The Whitespace or Comment to encode.
    """
    match wsc:
        case LineStyleComment():
            return f"//{wsc}"
        case BlockStyleComment():
            return f"/*{wsc}*/"
        case HashStyleComment():
            return f"/*{wsc}*/"
        case WhiteSpace():
            return str(wsc)
    raise NotImplementedError(f"Unknown whitespace or comment type: {wsc!r}")


_params = {
    "lexer": "basic",
    "parser": "lalr",
    "start": "wschs",
    "maybe_placeholders": False,
    "regex": True,
}

if not DEBUG:
    _params["transformer"] = transformer

parser = Lark.open("grammar/wsc.lark", rel_to=__file__, **_params)
