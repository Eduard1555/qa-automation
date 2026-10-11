import pytest
from fastapi.testclient import TestClient

import database
import main

@pytest.fixture
def client(tmp_path, monkeypatch):
    test_database_path = tmp_path / "test_qa_automation.db"

    monkeypatch.setattr(
        database,
        "DATABASE_PATH",
        test_database_path,
    )

    with TestClient(main.app) as test_client:
        yield test_client