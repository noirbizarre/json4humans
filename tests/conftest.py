from __future__ import annotations

from pathlib import Path
from types import ModuleType
from typing import Any

import pytest

from json4humans import json, json5, jsonc
from json4humans.types import JSONModule


def module_name(mod: ModuleType) -> str:
    return mod.__name__.split(".")[-1]


JSONS: dict[str, JSONModule] = {module_name(mod): mod for mod in (json, jsonc, json5)}
FIXTURES: Path = Path(__file__).parent / "fixtures"


class JSONTester:
    """
    Wraps a JSONModule and adds test helper to it.
    """

    module: JSONModule

    def __init__(self, module: JSONModule):
        self.module = module

    def assert_parse_equal(self, input: Path | str, expected: Any) -> Any:
        __tracebackhide__ = True
        data = self.module.loads(input.read_text() if isinstance(input, Path) else input)
        assert data == expected
        return data

    def __getattr__(self, name: str) -> Any:
        return getattr(self.module, name)


def pytest_generate_tests(metafunc: pytest.Metafunc):
    if "jsont" in metafunc.fixturenames:
        jsont_params: list[pytest.ParameterSet] = []

        if marker := metafunc.definition.get_closest_marker("jsons"):
            for name in marker.args:
                mod = JSONS[name]
                marks = [
                    getattr(pytest.mark, name),
                ]
                jsont_params.append(pytest.param(JSONTester(mod), id=name, marks=marks))
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
