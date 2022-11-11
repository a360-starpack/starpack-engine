import docker
from typing import Dict, Any
from ...schemas.payloads import Metadata

def tag_image(image: docker.models.images.Image, metadata: Metadata, step_data: Dict[str, Any]):

    image_name = step_data.get("image_name", metadata.name)
    image_tags = step_data.get("image_tags")

    if not image_name:
        image_name = metadata.name

    if image_tags:
        for tag in image_tags:
            image.tag(image_name, tag)
    else:
        image.tag(image_name)
    
    return {}

    

    
