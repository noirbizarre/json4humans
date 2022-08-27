"""
These tests are mostly trying to parse samples from
the official website: https://hjson.github.io/
as well as JSON and JSONC sample for backward compatibility
"""
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from tests.conftest import JSONTester


pytestmark = pytest.mark.jsons("hjson")


def test_tldr_example(jsont: JSONTester):
    json_as_str = """
    {
        # TL;DR
        human:   Hjson
        machine: JSON
    }
    """
    jsont.assert_parse_equal(
        json_as_str,
        {
            "human": "Hjson",
            "machine": "JSON",
        },
    )


def test_no_commas(jsont: JSONTester):
    json_as_str = """
    {
        first: 1
        second: 2
    }
    """
    jsont.assert_parse_equal(
        json_as_str,
        {
            "first": 1,
            "secomd": 2,
        },
    )


def test_comments(jsont: JSONTester):
    json_as_str = """
    {
        # hash style comments
        # (because it's just one character)

        // line style comments
        // (because it's like C/JavaScript/...)

        /* block style comments because
            it allows you to comment out a block */

        # Everything you do in comments,
        # stays in comments ;-}
    }
    """
    jsont.assert_parse_equal(json_as_str, {})


def test_identifier_keys(jsont: JSONTester):
    json_as_str = """
    {
        # specify rate in requests/second
        rate: 1000
    }
    """
    jsont.assert_parse_equal(
        json_as_str,
        {
            "rate": 1000,
        },
    )


def test_quoteless_strings(jsont: JSONTester):
    json_as_str = r"""
    {
        JSON: "a string",

        Hjson: a string

        # notice, no escape necessary:
        RegEx: \s+
    }
    """
    jsont.assert_parse_equal(
        json_as_str, {"JSON": "a string", "Hjson": "a string", "RegEx": r"\s+"}
    )


def test_punctuators(jsont: JSONTester):
    json_as_str = """
    {
        "key name": "{ sample }"
        "{}": " spaces at the start/end "
        this: is OK though: {}[],:
    }
    """
    jsont.assert_parse_equal(
        json_as_str,
        {
            "key name": "{ sample }",
            "{}": " spaces at the start/end ",
            "this": "is OK though: {}[],:",
        },
    )


def test_hjson_sample(jsont: JSONTester):
    json_as_str = """
    {
        // use #, // or /**/ comments,
        // omit quotes for keys
        key: 1
        // omit quotes for strings
        contains: everything on this line
        // omit commas at the end of a line
        cool: {
            foo: 1
            bar: 2
        }
        // allow trailing commas
        list: [
            1,
            2,
        ]
        // and use multiline strings
        realist:
            '''
            My half empty glass,
            I will fill your empty half.
            Now you are half full.
            '''
    }
    """
    jsont.assert_parse_equal(
        json_as_str,
        {
            "key": 1,
            "contains": "everything on this line",
            "cool": {
                "foo": 1,
                "bar": 2,
            },
            "list": [1, 2],
            "realist": "My half empty glass,\nI will fill your empty half.\nNow you are half full.",
        },
    )
