from __future__ import annotations

import pytest

from json4humans import wsc
from json4humans.types import WSC, BlockStyleComment, HashStyleComment, LineStyleComment, WhiteSpace


@pytest.mark.parametrize(
    "items,expected",
    (
        (None, []),
        ([], []),
        ([WhiteSpace(" ")], [WhiteSpace(" ")]),
        ([" "], [WhiteSpace(" ")]),
        (["  ", WhiteSpace(" ")], [WhiteSpace("  "), WhiteSpace(" ")]),
        (["// line comment"], [LineStyleComment(" line comment")]),
        (["  // line comment"], [WhiteSpace("  "), LineStyleComment(" line comment")]),
        (["/* block comment */"], [BlockStyleComment(" block comment ")]),
        (
            [
                """/*
      multiline block comment
      */"""
            ],
            [BlockStyleComment("\n      multiline block comment\n      ")],
        ),
        (["# Hash comment // /**/ #"], [HashStyleComment(" Hash comment // /**/ #")]),
    ),
)
def test_parse_wsc_list(items: list[WSC | str] | None, expected: list[WSC]):
    assert wsc.parse_list(items) == expected
