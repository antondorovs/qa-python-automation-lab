from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

import pytest

from qa_python_lab.mock_api import local_server

pytest_plugins = ["qa_python_lab.pytest_reporter"]


@pytest.fixture
def base_url() -> Iterator[str]:
    with local_server() as url:
        yield url


@pytest.fixture
def fixture_sql() -> Path:
    return Path(__file__).resolve().parents[1] / "data" / "fixture.sql"
