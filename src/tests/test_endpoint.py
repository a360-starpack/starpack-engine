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


def test_example_plugin(testclient: TestClient) -> None:
    response = testclient.post("/plugins/test/example_plugin", json={})

    print(response.content)
    assert response.status_code == 200


fake_input = {
    "package": {
        "metadata": {
            "name": "test",
            "version": "test"
        },
        "artifacts": {
                "root_location": "test",
                "inference": {
                    "function_name": "test",
                    "script_name": "test"
                }
            },
        "steps": [
            {"name": "example_plugin"}
        ]
    },
    "deployment": {
            "metadata": {
                "name": "test",
                "version": "test"
            },
            "artifacts": {
                "root_location": "test",
                "inference": {
                    "function_name": "test",
                    "script_name": "test"
                }
            },
            "steps": [
                {"name": "example_plugin"}
            ]
        }
}


def test_deploy_endpoint(testclient: TestClient) -> None:
    response = testclient.post("/deploy", json=fake_input)

    print(response.content)
    assert response.status_code == 200


def test_package_endpoint(testclient: TestClient) -> None:
    response = testclient.post("/package", json=fake_input)

    print(response.content)
    assert response.status_code == 200
