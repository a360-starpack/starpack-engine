from pathlib import Path
from typing import Optional, List

from pydantic import BaseModel, Extra

from .._config import settings


# Generic metadata
class Metadata(BaseModel):
    name: str
    description: Optional[str]
    version: Optional[str]
    author: Optional[str]
    author_email: Optional[str]


# Package-specific schema
class Inference(BaseModel):
    function_name: str
    script_name: str
    model_data: Optional[str]


class Artifacts(BaseModel):
    root_location: str
    validation_data: Optional[str]
    training_data: Optional[str]
    inference: Inference
    dependencies: Optional[str]
    streamlit: Optional[str]
    gradio_script_name: Optional[str]
    gradio_interface_name: Optional[str]

    @property
    def root_filepath(self) -> Path:
        return Path(f"{settings.root_path}/external/artifacts/{self.root_location}")


class Step(BaseModel):
    name: str
    version: Optional[str]

    class Config:
        extra = Extra.allow


class PackageInput(BaseModel):
    metadata: Metadata
    artifacts: Artifacts
    steps: List[Step]


# Deployment schema information
class DeployInput(BaseModel):
    metadata: Metadata
    steps: List[Step]


# Overall Input Schema
# TODO: Credentials schema
class StarpackInput(BaseModel):
    package: Optional[PackageInput]
    deployment: Optional[DeployInput]
