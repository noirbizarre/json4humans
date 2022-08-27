from __future__ import annotations

from pathlib import Path

import pytest


@pytest.fixture
def fixtures(fixtures: Path) -> Path:
    return fixtures / "jsonc"
