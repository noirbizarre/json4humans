from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from tests.conftest import JSONTester

if TYPE_CHECKING:
    from pytest_benchmark.fixture import BenchmarkFixture


pytestmark = pytest.mark.jsons("json", "jsonc", "json5")


@pytest.mark.benchmark(group="json-dumps")
@pytest.mark.fixturize("json/benchs/*.json")
def bench_json_dumps(benchmark: BenchmarkFixture, jsont: JSONTester, fixture: Path):
    benchmark.name = jsont.name
    benchmark.fullname = f"dumps({fixture.stem}.json)"

    data = jsont.loads(fixture.read_text())

    benchmark(jsont.dumps, data)


@pytest.mark.fixturize("json/benchs/*.json")
@pytest.mark.benchmark(group="json-loads")
def bench_json_loads(benchmark: BenchmarkFixture, jsont: JSONTester, fixture: Path):
    benchmark.name = jsont.name
    benchmark.fullname = f"loads({fixture.stem}.json)"

    data = fixture.read_text()

    benchmark(jsont.loads, data)
