import pytest
from fastapi.testclient import TestClient
from src.engine.main import app


@pytest.fixture
def testclient():
    return TestClient(app)


def test_healthcheck(testclient: TestClient) -> None:
    response = testclient.get("/healthcheck")
    assert response.status_code == 200
    assert response.json() == {"healthy": True}


def test_refresh_plugins(testclient: TestClient) -> None:
    response = testclient.patch("/plugins")
    assert response.status_code == 202
