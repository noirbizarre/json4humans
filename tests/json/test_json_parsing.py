from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

import pytest

if TYPE_CHECKING:
    from tests.conftest import JSONTester


pytestmark = pytest.mark.jsons(
    "json",
    "jsonc",
    "json5",
)


LITERALS = (
    pytest.param("true", True, id="bool:true"),
    pytest.param("false", False, id="bool:false"),
    pytest.param("null", None, id="null"),
    pytest.param('"foo"', "foo", id="string"),
    pytest.param('"\\u00DC"', "Ü", id="string:unicode"),
    pytest.param(
        '"\\"-\\\\-\\/-\\b-\\f-\\n-\\r-\\t"', '"-\\-/-\b-\f-\n-\r-\t', id="string:escaped"
    ),
    pytest.param("9", 9, id="int"),
    pytest.param("-9", -9, id="int:negative"),
    pytest.param("0.129", 0.129, id="float"),
    pytest.param("23e3", 23e3, id="float:exp"),
    pytest.param("1.2E+3", 1.2e3, id="float:positive-exp"),
    pytest.param("1.2E-3", 1.2e-3, id="float:negative-exp"),
    pytest.param("-1.2E+3", -1.2e3, id="float:signed-positive-exp"),
    pytest.param("-1.2E-3", -1.2e-3, id="float:signed-negative-exp"),
)


@pytest.mark.parametrize("value,expected", LITERALS)
def test_parse_literal(value: str, expected: Any, jsont: JSONTester):
    jsont.assert_parse_equal(value, expected)


def test_parse_objects(jsont: JSONTester):
    jsont.assert_parse_equal("{}", {})
    jsont.assert_parse_equal('{ "foo": true }', {"foo": True})
    jsont.assert_parse_equal('{ "bar": 8, "xoo": "foo" }', {"bar": 8, "xoo": "foo"})
    jsont.assert_parse_equal('{ "hello": [], "world": {} }', {"hello": [], "world": {}})
    jsont.assert_parse_equal(
        '{ "a": false, "b": true, "c": [ 7.4 ] }', {"a": False, "b": True, "c": [7.4]}
    )
    jsont.assert_parse_equal(
        """
        {
            "lineComment": "//",
            "blockComment": ["/*", "*/"],
            "brackets": [ ["{", "}"], ["[", "]"], ["(", ")"] ]
        }
        """,
        {
            "lineComment": "//",
            "blockComment": ["/*", "*/"],
            "brackets": [["{", "}"], ["[", "]"], ["(", ")"]],
        },
    )
    jsont.assert_parse_equal('{ "hello": [], "world": {} }', {"hello": [], "world": {}})
    jsont.assert_parse_equal(
        '{ "hello": { "again": { "inside": 5 }, "world": 1 }}',
        {"hello": {"again": {"inside": 5}, "world": 1}},
    )
    jsont.assert_parse_equal('{ "": true }', {"": True})


def test_parse_arrays(jsont: JSONTester):
    jsont.assert_parse_equal("[]", [])
    jsont.assert_parse_equal("[ [],  [ [] ]]", [[], [[]]])
    jsont.assert_parse_equal("[ 1, 2, 3 ]", [1, 2, 3])
    jsont.assert_parse_equal('[ { "a": null } ]', [{"a": None}])


def test_parse_as_std_json(jsont: JSONTester):
    json_as_string = """
    {
        "str": "abcd",
        "int": 42,
        "bool": true,
        "list": [1, 2, 3, 4],
        "nested": {"key": "value"}
    }
    """
    assert jsont.loads(json_as_string) == json.loads(json_as_string)


def test_dump_as_std_json(jsont: JSONTester):
    json_as_obj = {
        "str": "abcd",
        "int": 42,
        "bool": True,
        "list": [1, 2, 3, 4],
        "tuple": (1, 2, 3, 4),
        "nested": {"key": "value"},
    }
    assert jsont.dumps(json_as_obj) == json.dumps(json_as_obj, separators=(",", ":"))
