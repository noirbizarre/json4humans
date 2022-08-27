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


pytestmark = pytest.mark.jsons("jsonc", "json5")


@pytest.mark.fixturize("jsonc/*.jsonc")
def test_load_and_dump_jsonc_with_style_preservation(jsont: JSONTester, fixture: Path):
    raw = fixture.read_text()
    parsed = jsont.loads(raw)
    print("parsed", parsed)
    assert jsont.dumps(parsed) == raw
