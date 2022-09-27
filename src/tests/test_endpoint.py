import pytest
from fastapi.testclient import TestClient
from src.starpack.main import app

@pytest.fixture
def testclient():
    return TestClient(app)

def test_hello_world(testclient):
    response = testclient.get("/hello_world")
    assert response.status_code == 200
    assert response.json() == {"hello": "world"}