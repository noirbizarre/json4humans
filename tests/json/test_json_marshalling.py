"""
These tests are mostly trying to parse samples from
the specifications: https://spec.json5.org/
as well as JSON and JSONC sample for backward compatibility
"""
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from tests.conftest import JSONTester


pytestmark = pytest.mark.jsons("json", "jsonc", "json5")


@pytest.mark.fixturize("json/*.json")
def test_load_and_dump_json_with_style_preservation(jsont: JSONTester, fixture: Path):
    raw = fixture.read_text()
    assert jsont.dumps(jsont.loads(raw)) == raw
