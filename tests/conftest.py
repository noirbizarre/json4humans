from __future__ import annotations

from pathlib import Path
from types import ModuleType
from typing import Any

import pytest

from json4humans import hjson, json, json5, jsonc
from json4humans.types import JSONModule


def module_name(mod: ModuleType) -> str:
    return mod.__name__.split(".")[-1]


JSONS: dict[str, JSONModule] = {module_name(mod): mod for mod in (json, jsonc, json5, hjson)}
FIXTURES: Path = Path(__file__).parent / "fixtures"


class JSONTester:
    json: JSONModule

    def __init__(self, json: JSONModule):
        self.json = json

    def assert_parse_equal(self, input: Path | str, expected: Any) -> Any:
        __tracebackhide__ = True
        data = self.json.loads(input.read_text() if isinstance(input, Path) else input)
        assert data == expected
        return data

    def loads(self, *args, **kwargs) -> Any:
        __tracebackhide__ = True
        return self.json.loads(*args, **kwargs)

    def load(self, *args, **kwargs) -> Any:
        __tracebackhide__ = True
        return self.json.load(*args, **kwargs)

    def dumps(self, *args, **kwargs) -> str:
        __tracebackhide__ = True
        return self.json.dumps(*args, **kwargs)

    def dump(self, *args, **kwargs) -> None:
        __tracebackhide__ = True
        return self.json.dump(*args, **kwargs)


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
