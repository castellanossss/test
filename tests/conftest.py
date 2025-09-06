# tests/conftest.py
import os
import sys
from pathlib import Path
import asyncio
import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

os.environ.setdefault("SKIP_DB_INIT_FOR_TESTS", "1")

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
def test_client():
    from app.main import app
    from fastapi.testclient import TestClient
    client = TestClient(app)
    try:
        yield client
    finally:
        app.dependency_overrides.clear()
