from typing import Dict, Any

import docker

from ...schemas.payloads import Metadata


def docker_deploy(
    image: docker.models.images.Image, metadata: Metadata, step_data: Dict[str, Any]
):
    client = docker.from_env()

    client.containers.run(
        image=image,
        name=metadata.name,
        tty=True,
        ports={80: step_data.get("port", 80)},
        stdin_open=True,
        detach=True,
        labels={
            "name": metadata.name,
            "version": metadata.version,
            "app": "starpack_package",
        },
    )
    return {}
