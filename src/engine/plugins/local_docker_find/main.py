import docker
from typing import Dict, Any


def docker_find(step_data: Dict[str, Any]):
    client = docker.from_env()

    if "image" in step_data:
        name = step_data["image"].get("name", "")
        tag = step_data["image"].get("tag", "latest")

    image = client.images.get(f"{name}:{tag}")

    return {"image": image}
