import docker

from typing import Dict, Any, Optional, Callable

def docker_format_filter(filter_items: Dict[str, Any]):
    return [f"{key}={value}" for key, value in filter_items.items()]


def generate_docker_url(container: docker.models.containers.Container) -> str:

    port_details = container.ports.values()

    if len(port_details) == 0:
        raise ValueError(
            f"The container, {container.name}, does not have any exposed ports"
        )

    # Assume there's only a single port exposed
    for value in port_details:
        port = value[0]["HostPort"]
        break

    return f"http://localhost:{port}"


def list_docker_package(
    name: Optional[str] = None,
    version: Optional[str] = None,
    wrapper: Optional[str] = None,
    client_factory: Callable = docker.from_env,
):
    client = client_factory()

    filters = {"app": "starpack_package"}

    if name:
        filters["name"] = name

    if version:
        filters["version"] = version

    if wrapper:
        filters["wrapper"] = wrapper

    containers = client.containers.list(
        filters={"label": docker_format_filter(filters)}, all=True
    )

    container_details = list()

    for container in containers:
        container_dict = container.labels
        container_dict["url"] = generate_docker_url(container)
        container_dict["docker_container_name"] = container.name

        container_details.append(container_dict)

    return container_details


def delete_docker_package(
    name: Optional[str] = None,
    version: Optional[str] = None,
    wrapper: Optional[str] = None,
    client_factory: Callable = docker.from_env,
):
    client = client_factory()

    filters = {"app": "starpack_package"}

    if name:
        filters["name"] = name

    if version:
        filters["version"] = version

    if wrapper:
        filters["wrapper"] = wrapper

    containers = client.containers.list(
        filters={"label": docker_format_filter(filters)}, all=True
    )

    for container in containers:
        container.remove(force=True)

    return {"status": f"Successfully removed {len(containers)} deployments!"}


def get_docker_package_logs(
    name: Optional[str] = None,
    version: Optional[str] = None,
    wrapper: Optional[str] = None,
    client_factory: Callable = docker.from_env,
):
    client = client_factory()

    filters = {"app": "starpack_package"}

    if name:
        filters["name"] = name

    if version:
        filters["version"] = version

    if wrapper:
        filters["wrapper"] = wrapper

    containers = client.containers.list(
        filters={"label": docker_format_filter(filters)}, all=True
    )

    if len(containers) != 1:
        raise ValueError(
            f"There were {len(containers)} containers found matching the query."
        )

    return containers[0].logs()
