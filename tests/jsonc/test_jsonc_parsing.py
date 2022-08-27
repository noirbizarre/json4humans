from __future__ import annotations

from typing import TYPE_CHECKING, Any

import pytest

from json4humans.types import BlockStyleComment, JSONType, LineStyleComment, WhiteSpace
from tests.json.test_json_parsing import LITERALS

if TYPE_CHECKING:
    from tests.conftest import JSONTester


pytestmark = pytest.mark.jsons(
    "jsonc",
    "json5",
)

LITERALS_WITH_COMMENTS = (
    *(
        pytest.param(
            f" /* block before */ {p.values[0]} /* block after */ // line after",
            p.values[1],
            id=p.id,
        )
        for p in LITERALS
    ),
)


@pytest.mark.parametrize("value,expected", LITERALS_WITH_COMMENTS)
def test_parse_literal_with_comments(value: str, expected: Any, jsont: JSONTester):
    parsed: JSONType = jsont.assert_parse_equal(value, expected)
    assert isinstance(parsed, JSONType)
    assert parsed.json_before == [
        WhiteSpace(" "),
        BlockStyleComment(" block before "),
        WhiteSpace(" "),
    ]
    assert parsed.json_after == [
        WhiteSpace(" "),
        BlockStyleComment(" block after "),
        WhiteSpace(" "),
        LineStyleComment(" line after"),
    ]


def test_parse_objects_with_comments(jsont: JSONTester):
    jsont.assert_parse_equal('{ "foo": /*hello*/true }', {"foo": True})


def test_parse_arrays_with_comments(jsont: JSONTester):
    jsont.assert_parse_equal("[]", [])
    jsont.assert_parse_equal("[ [],  [ [] ]]", [[], [[]]])
    jsont.assert_parse_equal("[ 1, 2, 3 ]", [1, 2, 3])
    jsont.assert_parse_equal('[ { "a": null } ]', [{"a": None}])


def test_parse_json_with_line_comments(jsont: JSONTester):
    json_as_string = """
    {
        // it's a string
        "str": "abcd",
        // it's an integer
        "int": 42,
        // it's a boolean
        "bool": true
    }
    """
    jsont.assert_parse_equal(
        json_as_string,
        {
            "str": "abcd",
            "int": 42,
            "bool": True,
        },
    )


def test_parse_json_with_block_comments(jsont: JSONTester):
    json_as_string = """
    {
        /* it's a string */
        "str": "abcd", /* still a string */
        /*
         it's an integer
         */
        "int": 42,
        /*it's a boolean*/
        "bool": true
    }
    """
    jsont.assert_parse_equal(
        json_as_string,
        {
            "str": "abcd",
            "int": 42,
            "bool": True,
        },
    )
