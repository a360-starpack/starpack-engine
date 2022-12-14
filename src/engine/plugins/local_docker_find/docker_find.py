from typing import Dict, Any, Optional

import docker
from fastapi import HTTPException

from ...schemas.payloads import Metadata


def docker_find(
    images: Dict[str, docker.models.images.Image],
    step_data: Dict[str, Any],
    package_metadata: Optional[Metadata] = None,
):
    client = docker.from_env()

    # Try to see if the package name/type is given and default to FastAPI
    # Since we support multiple package types, we look for the package name and default
    wrapper_type = step_data.get("wrapper", "fastapi")

    # Try to grab the name and tag from the metadata
    name = ""
    tag = ""
    if step_data.get("image"):
        name = step_data["image"].get("name", "")
        tag = step_data["image"].get("tag", "")

    if not tag and package_metadata and package_metadata.version:
        tag = package_metadata.version
    elif not tag:
        tag = "latest"

    # if they didn't provide a name, we'll grab one from the package metadata we got
    if not name and package_metadata:
        name = package_metadata.name

    # If we still don't have it, let's raise an exception
    if not name:
        raise HTTPException(
            status_code=400,
            detail="Unable to parse an image name or the package name from the given payload. "
            "Please specify an image name in the `local_docker_find` step or "
            "include the package information that goes with this request.",
        )

    image_name = f"{name}-{wrapper_type}:{tag}"

    try:
        image = client.images.get(image_name)
    except docker.errors.ImageNotFound:
        raise HTTPException(
            status_code=404,
            detail=f"Unable to find the package, '{image_name}'. Please package your model and try again.",
        )

    images[wrapper_type] = image

    return images
