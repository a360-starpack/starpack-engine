from typing import Dict, Any, Optional

import docker
from fastapi import HTTPException

from ...schemas.payloads import Metadata


def docker_find(step_data: Dict[str, Any], package_metadata: Optional[Metadata] = None):
    client = docker.from_env()

    # Try to grab the name and tag from the metadata
    name = ""
    tag = "latest"
    if step_data.get("image"):
        name = step_data["image"].get("name", "")
        tag = step_data["image"].get("tag", "latest")

    if not tag:
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
    try:
        image = client.images.get(f"{name}:{tag}")
    except docker.errors.ImageNotFound:
        raise HTTPException(
            status_code=404,
            detail=f"Unable to find the package, '{name}:{tag}'. "
            f"Please package your model and try again.",
        )

    return {"image": image}
