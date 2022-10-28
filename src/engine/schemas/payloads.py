from pathlib import Path
from pydantic import BaseModel, Field, Extra
from typing import Optional, List
from engine._config import settings

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
class DeploymentTarget(BaseModel):
    type: str
    environment: Optional[str]


class DeployInput(BaseModel):
    metadata: Metadata
    deployment_target: DeploymentTarget
    version: Optional[str]
    model_endpoint: Optional[str]


# Overall Input Schema
# TODO: Credentials schema
class StarpackInput(BaseModel):
    package: Optional[PackageInput]
    deployment: Optional[DeployInput]
