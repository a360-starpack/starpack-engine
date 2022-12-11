from typing import Dict, Any, Optional
import socket
from fastapi import HTTPException
import docker

from ...schemas.payloads import Metadata


def find_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(('localhost', 0))
        port = sock.getsockname()[1]

    return port


def delete_duplicate_containers(
    client: docker.APIClient, label_filter: Dict[str, Any]
) -> None:

    docker_formatted_filter = docker_format_filter(label_filter)

    matching_deployments = client.containers.list(
        filters={"label": docker_formatted_filter}, all=True
    )

    for container in matching_deployments:
        container.remove(force=True)


def docker_format_filter(filter_items: Dict[str, Any]):
    return [f"{key}={value}" for key, value in filter_items.items()]


def create_wrapper_container(
    client: docker.APIClient,
    images: Dict[str, docker.models.images.Image],
    metadata: Metadata,
    wrapper: str,
    port: Optional[int] = None,
) -> Dict[str, str]:
    try:
        image = images[wrapper]
    except KeyError:
        raise HTTPException(
            status_code=400,
            detail=f"Unable to deploy wrapper {wrapper}. Please add the `wrapper` field to `local_docker_deploy` "
            "step and ensure that it points to the proper package type.",
        )

    if not port:
        # Find and deploy on an open port
        port = find_free_port()

    labels = {
        "name": metadata.name,
        "version": metadata.version,
        "app": "starpack_package",
        "wrapper": wrapper,
    }

    # Remove any matching containers
    delete_duplicate_containers(client, labels)
    try:
        client.containers.run(
            image=image,
            name=f"{metadata.name}-{wrapper}-{metadata.version}",
            tty=True,
            ports={80: port},
            stdin_open=True,
            detach=True,
            labels=labels,
        )
    except docker.errors.APIError:
        raise HTTPException(400, detail=f"The port, {port}, was already in use and unable to be allocated. "
                                        f"Please remove your port information and one will be automatically allocated.")
    return {wrapper: f"http://localhost:{port}"}


def docker_deploy(
    images: Dict[str, docker.models.images.Image],
    metadata: Metadata,
    step_data: Dict[str, Any],
) -> Dict[str, Optional[Dict[str, str]]]:
    client = docker.from_env()

    # See if we were given a port
    port = step_data.get("port")

    # Since we support multiple package types, we look for the package name and default
    wrappers = step_data.get("wrapper")

    if not wrappers:
        if len(images) == 1:
            wrappers = [{"name": list(images.keys())[0], "port": port}]
        else:
            wrappers = [{"name": "fastapi", "port": port}]


    endpoints = dict()
    for wrapper_type in wrappers:
        endpoint = create_wrapper_container(
            client=client,
            images=images,
            metadata=metadata,
            wrapper=wrapper_type.get("name"),
            port=wrapper_type.get("port", port),
        )
        endpoints.update(endpoint)

    return {"endpoints": endpoints}
