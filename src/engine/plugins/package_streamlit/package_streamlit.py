from pathlib import Path
from string import Template
from typing import Optional, Dict

import docker
from pydantic import BaseModel

from ...schemas.payloads import Artifacts, Metadata, Inference


class WrapperYAML(BaseModel):
    name: str
    version: Optional[str]
    description: Optional[str]
    validation_data: Optional[str]
    inference: Inference


def package(
    images: Dict[str, docker.models.images.Image],
    artifacts: Artifacts,
    metadata: Metadata,
    custom_input: str = "",
):
    # Write the YAML information to the package
    artifacts_location = artifacts.root_filepath

    yaml_input = WrapperYAML(
        name=metadata.name,
        version=metadata.version,
        description=metadata.description,
        inference=artifacts.inference,
        validation_data=artifacts.validation_data,
    )

    yaml_path = artifacts_location / "starpack.yaml"
    yaml_path.write_text(yaml_input.json())

    # Create Dockerfile
    dockerfile_template_mapping = {
        "dependency_install": "",
        "custom_input": custom_input if custom_input else "",
        "streamlit_script": artifacts.streamlit,
    }

    if artifacts.dependencies:
        dockerfile_template_mapping[
            "dependency_install"
        ] = f"RUN pip install -r /app/{artifacts.dependencies}"

    dockerfile_template = Path(__file__).parent / "templates" / "template.Dockerfile"

    dockerfile = Template(dockerfile_template.read_text()).substitute(
        dockerfile_template_mapping
    )

    dockerfile_path = artifacts_location / "Dockerfile"
    dockerfile_path.write_text(dockerfile)

    # Write Dockerfile
    client = docker.from_env()

    image = client.images.build(
        path=str(artifacts_location),
        labels={"app": "starpack-model", "model-name": metadata.name, "version": metadata.version},
        tag=f"{metadata.name}-streamlit:{metadata.version}",
    )

    images["streamlit"] = image[0]

    return images
