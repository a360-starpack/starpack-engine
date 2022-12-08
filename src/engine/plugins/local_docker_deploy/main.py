from typing import Dict, Any
import socket

import docker

from ...schemas.payloads import Metadata


def find_free_port(port: int = 2000) -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        result = sock.connect_ex(("localhost", port))
    if result != 0:
        # Port isn't in use, we can return it
        return port
    else:
        print(result)
        # Increment and try again
        return find_free_port(port + 1)


def delete_duplicate_containers(
    client: docker.client, label_filter: Dict[str, Any]
) -> None:

    docker_formatted_filter = docker_format_filter(label_filter)

    matching_deployments = client.containers.list(
        filters={"label": docker_formatted_filter}, all=True
    )

    for container in matching_deployments:
        container.remove(force=True)


def docker_format_filter(filter_items: Dict[str, Any]):
    return [f"{key}={value}" for key, value in filter_items.items()]


def docker_deploy(
    image: docker.models.images.Image, metadata: Metadata, step_data: Dict[str, Any]
):
    client = docker.from_env()

    port = step_data.get("port")

    if not port:
        # Find and deploy on an open port
        port = find_free_port()

    labels = {
        "name": metadata.name,
        "version": metadata.version,
        "app": "starpack_package",
    }

    # Remove any matching containers
    delete_duplicate_containers(client, labels)

    client.containers.run(
        image=image,
        name=f"{metadata.name}-{metadata.version}",
        tty=True,
        ports={80: port},
        stdin_open=True,
        detach=True,
        labels=labels,
    )
    return {"endpoint": f"http://localhost:{port}"}
