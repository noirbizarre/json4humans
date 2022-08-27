"""
These tests are mostly trying to parse samples from
the specifications: https://spec.json5.org/
as well as JSON and JSONC sample for backward compatibility
"""
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

import pytest

from json4humans import json5

if TYPE_CHECKING:
    from tests.conftest import JSONTester


pytestmark = pytest.mark.jsons("json5")


def test_parse_json5_short_exemple(jsont: JSONTester, fixtures: Path):
    jsont.assert_parse_equal(
        fixtures / "sample.json5",
        json5.Object(
            [
                (json5.Ident("unquoted"), json5.String("and you can quote me on that", quote="'")),
                (
                    json5.Ident("singleQuotes"),
                    json5.String('I can use "double quotes" here', quote="'"),
                ),
                (
                    json5.Ident("lineBreaks"),
                    json5.String(
                        "Look, Mom! \
No \\n's!"
                    ),
                ),
                (json5.Ident("hexadecimal"), json5.HexInteger(0xDECAF)),
                (json5.Ident("leadingDecimalPoint"), json5.Float(0.8675309)),
                (json5.Ident("andTrailing"), json5.Float(8675309.0)),
                (json5.Ident("positiveSign"), json5.Integer(+1)),
                (json5.Ident("trailingComma"), json5.String("in objects", quote="'")),
                (
                    json5.Ident("andIn"),
                    json5.Array(
                        [
                            json5.String("arrays", quote="'"),
                        ]
                    ),
                ),
                (json5.String("backwardsCompatible"), json5.String("with JSON")),
            ]
        ),
    )


def test_parse_json5_dict_equal(jsont: JSONTester, fixtures: Path):
    jsont.assert_parse_equal(
        fixtures / "sample.json5",
        {
            "unquoted": "and you can quote me on that",
            "singleQuotes": 'I can use "double quotes" here',
            "lineBreaks": "Look, Mom! \
No \\n's!",
            "hexadecimal": 0xDECAF,
            "leadingDecimalPoint": 0.8675309,
            "andTrailing": 8675309.0,
            "positiveSign": +1,
            "trailingComma": "in objects",
            "andIn": ["arrays"],
            "backwardsCompatible": "with JSON",
        },
    )


@pytest.mark.parametrize(
    "source,expected",
    (
        pytest.param('{key: "value",}', {"key": "value"}, id="object"),
        pytest.param('["value",]', ["value"], id="array"),
        pytest.param(
            '{key: {key: ["value",["value,value",],],},}',
            {"key": {"key": ["value", ["value,value"]]}},
            id="mixed",
        ),
    ),
)
def test_trailing_comma(jsont: JSONTester, source: str, expected: Any):
    jsont.assert_parse_equal(source, expected)
