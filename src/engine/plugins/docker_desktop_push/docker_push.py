from typing import Dict, Any

import docker
from fastapi import HTTPException

from ...schemas.payloads import Metadata


def tag_image(
    images: Dict[str, docker.models.images.Image],
    metadata: Metadata,
    step_data: Dict[str, Any],
):
    image_name = step_data.get("image_name", metadata.name)
    image_tags = step_data.get("image_tags")

    # Since we support multiple package types, we look for the package name and default
    starpack_image = step_data.get("package", "fastapi")

    if len(images) == 1:
        # If we only have one image, we can assume it's that image type
        starpack_image = list(step_data.keys())[0]

    try:
        image = images[starpack_image]
    except KeyError:
        print(images)
        raise HTTPException(
            status_code=400,
            detail="Unable to push package. Please add the `package` field to `docker_desktop_push` "
            "step and ensure that it points to the proper package type.",
        )

    if not image_name:
        image_name = metadata.name

    if image_tags:
        for tag in image_tags:
            image.tag(image_name, tag)
    else:
        image.tag(image_name)

    return {}
