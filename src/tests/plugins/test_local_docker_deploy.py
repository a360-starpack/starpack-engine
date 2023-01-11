import pytest
from fastapi import HTTPException

from src.engine.plugins.local_docker_deploy.docker_deploy import (
    find_free_port,
    delete_duplicate_containers,
    docker_format_filter,
    docker_deploy,
)
from src.engine.schemas.payloads import Metadata


def test_docker_format_filter():
    test_dict = {
        "okay": "yeah",
        "this": "is_cool",
        "final": "pair"
    }

    output = ["okay=yeah", "this=is_cool", "final=pair"]

    assert output == docker_format_filter(test_dict)
