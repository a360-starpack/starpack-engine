import pytest
import docker
from fastapi import HTTPException

from src.engine.plugins.local_docker_find.docker_find import docker_find
from src.engine.schemas.payloads import Metadata


class FakeContainer:
    labels = {
        "desktop.docker.io/wsl-distro": "Ubuntu-20.04",
        "app": "starpack-engine",
    }
    attrs = {
        "HostConfig": {
            "PortBindings": {"1976/tcp": [{"HostIp": "", "HostPort": "1976"}]},
        }
    }

    status = "running"

    def remove(*args, **kwargs):
        ...

    def put_archive(*args, **kwargs):
        ...


class FakeContainerModule:
    def list(*args, **kwargs):
        return [FakeContainer]

    def run(*args, **kwargs):
        pass


class FakeImageModule:
    @staticmethod
    def get(name: str):
        return name

    def pull(*args):
        pass


class FakeVolume:
    def remove(*args, **kwargs):
        ...


class FakeVolumesModule:
    def get(*args, **kwargs):
        return FakeVolume()

    def create(*args, **kwargs):
        ...


class FakeDockerClient:
    def __init__(self, *args, **kwargs) -> None:
        self.containers = FakeContainerModule
        self.images = FakeImageModule
        self.volumes = FakeVolumesModule


@pytest.fixture(autouse=True)
def mock_docker(monkeypatch):
    monkeypatch.setattr(docker, "from_env", FakeDockerClient)


def test_docker_find_default():
    name = "test-name"
    tag = "test-tag"
    step_data = {"image": {"name": name, "tag": tag}}
    images = dict()
    output = docker_find(images, step_data)

    assert output == {"fastapi": f"{name}-fastapi:{tag}"}


def test_docker_find_empty():
    step_data = dict()
    images = dict()
    with pytest.raises(HTTPException) as e:
        docker_find(images, step_data)

    assert e.value.status_code == 400


def test_docker_find_no_tag():
    name = "test-name"
    tag = None
    step_data = {"image": {"name": name, "tag": tag}}
    images = dict()
    output = docker_find(images, step_data)

    assert output == {"fastapi": f"{name}-fastapi:latest"}


def test_docker_find_no_image(monkeypatch):
    def fake_get(*args):
        raise docker.errors.ImageNotFound(message="test")

    monkeypatch.setattr(FakeImageModule, "get", fake_get)
    name = "test-name"
    tag = "test-tag"
    step_data = {"image": {"name": name, "tag": tag}}
    images = dict()
    with pytest.raises(HTTPException) as e:
        docker_find(images, step_data)

    assert e.value.status_code == 404


def test_docker_find_with_package_metadata():
    name = "test-name"
    step_data = dict()
    images = dict()
    metadata = Metadata(name=name)
    output = docker_find(images, step_data, metadata)

    assert output == {"fastapi": f"{name}-fastapi:latest"}
