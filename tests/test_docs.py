from __future__ import annotations

from pathlib import Path

import pytest

DOCS: Path = Path(__file__).parent.parent / "docs"
SNIPPETS: Path = DOCS / "snippets"


def snippet_id(snippet: Path) -> str:
    return str(snippet.relative_to(SNIPPETS).with_suffix(""))


def exec_python(source):
    """Exec the python source given in a new module namespace
    Does not return anything, but exceptions raised by the source
    will propagate out unmodified
    """
    try:
        exec(source, {"__MODULE__": "__main__"})
    except Exception:
        print(source)
        raise


@pytest.mark.parametrize("snippet", SNIPPETS.glob("**/*.py"), ids=snippet_id)
def test_snippets(snippet: Path):
    # exec_python(snippet.read_text())
    exec(snippet.read_text(), {"__MODULE__": "__main__"})
