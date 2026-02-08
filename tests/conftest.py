import sqlite3
from contextlib import asynccontextmanager

import pytest
from fastapi.testclient import TestClient

from app.database import get_db, init_db
from app.main import app
from app.utils import CODE_LENGTH


@pytest.fixture
def client(tmp_path):
    db_file = tmp_path / "test.db"

    def override_get_db():
        conn = sqlite3.connect(db_file)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    app.dependency_overrides[get_db] = override_get_db

    @asynccontextmanager
    async def test_lifespan(app):
        init_db(db_file)
        yield

    original_lifespan = app.router.lifespan_context
    app.router.lifespan_context = test_lifespan

    try:
        with TestClient(app) as client:
            yield client
    finally:
        app.router.lifespan_context = original_lifespan
        app.dependency_overrides.clear()


@pytest.fixture
def example_url():
    return "https://example.com/"


@pytest.fixture
def url_payload(example_url):
    return {"full_url": example_url}


@pytest.fixture
def code_length():
    return CODE_LENGTH
