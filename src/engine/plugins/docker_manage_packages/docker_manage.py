import docker

from typing import Dict, Any, Optional, Callable


def docker_format_filter(filter_items: Dict[str, Any]):
    return [f"{key}={value}" for key, value in filter_items.items()]


def list_docker_package(
    name: Optional[str] = None,
    version: Optional[str] = None,
    wrapper: Optional[str] = None,
    client_factory: Callable = docker.from_env,
):
    client = client_factory()

    filters = {"app": "starpack-model"}

    if name:
        filters["name"] = name

    if version:
        filters["version"] = version

    if wrapper:
        filters["wrapper"] = wrapper

    images = client.images.list(
        filters={"label": docker_format_filter(filters)},
    )

    image_details = list()

    for image in images:
        image_dict = image.labels

        image_details.append(image_dict)

    return image_details


def delete_docker_package(
    name: Optional[str] = None,
    version: Optional[str] = None,
    wrapper: Optional[str] = None,
    client_factory: Callable = docker.from_env,
):
    client = client_factory()

    filters = {"app": "starpack-model"}

    if name:
        filters["name"] = name

    if version:
        filters["version"] = version

    if wrapper:
        filters["wrapper"] = wrapper

    images = client.images.list(
        filters={"label": docker_format_filter(filters)},
    )

    for image in images:
        image.remove(force=True)

    return {"status": f"Successfully removed images: {len(images)}"}
