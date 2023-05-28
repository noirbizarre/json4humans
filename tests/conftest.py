from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from json4humans import json, json5, jsonc
from json4humans.protocol import JSONModule

JSON_MODULES = (
    json,
    jsonc,
    json5,
)

FIXTURES: Path = Path(__file__).parent / "fixtures"


class JSONTester:
    """
    Wraps a JSONModule and adds test helper to it.
    """

    module: JSONModule

    def __init__(self, module: JSONModule):
        self.module = module

    @property
    def name(self) -> str:
        return self.module.__name__.split(".")[-1]

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"JSONTester({self.module.__name__})"

    def assert_parse_equal(self, input: Path | str, expected: Any) -> Any:
        __tracebackhide__ = True
        data = self.module.loads(input.read_text() if isinstance(input, Path) else input)
        assert data == expected
        return data

    def __getattr__(self, name: str) -> Any:
        return getattr(self.module, name)


JSONS: dict[str, JSONTester] = {
    tester.name: tester for tester in (JSONTester(module) for module in JSON_MODULES)
}


def pytest_generate_tests(metafunc: pytest.Metafunc):
    if "jsont" in metafunc.fixturenames:
        jsont_params: list[pytest.ParameterSet] = []

        if marker := metafunc.definition.get_closest_marker("jsons"):
            for name in marker.args:
                tester = JSONS[name]
                marks = [
                    getattr(pytest.mark, name),
                ]
                jsont_params.append(pytest.param(tester, id=name, marks=marks))
        metafunc.parametrize("jsont", jsont_params)

    if "fixture" in metafunc.fixturenames:
        fixture_params: list[pytest.ParameterSet] = []

        if marker := metafunc.definition.get_closest_marker("fixturize"):
            pattern = marker.args[0]
            for file in FIXTURES.glob(pattern):
                fixture_params.append(pytest.param(file, id=file.stem))
        metafunc.parametrize("fixture", fixture_params)


@pytest.fixture
def fixtures() -> Path:
    return FIXTURES
