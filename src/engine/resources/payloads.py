from pydantic import BaseModel, Field, Extra
from typing import Optional, List


class Metadata(BaseModel):
    name: str
    version: Optional[str]
    author: Optional[str]
    author_email: Optional[str] = Field(None, alias="author-email")


class Inference(BaseModel):
    function_name: str = Field(..., alias="function-name")
    script_name: str = Field(..., alias="script-name")


class Artifacts(BaseModel):
    root_location: str = Field(..., alias="root-location")
    model_data: Optional[List[str]] = Field(None, alias="model-data")
    validation_data: Optional[str] = Field(None, alias="validation-data")
    training_data: Optional[str] = Field(None, alias="training-data")
    inference: Inference
    dependencies: Optional[str]


class Step(BaseModel):
    type: str

    class Config:
        extra = Extra.allow


class PackageInput(BaseModel):
    metadata: Metadata
    artifacts: Artifacts
    steps: List[Step]


class DeploymentTarget(BaseModel):
    type: str
    environment: Optional[str]


class DeployInput(BaseModel):
    metadata: Metadata
    deployment_target: DeploymentTarget = Field(..., alias="deployment-target")
    version: Optional[str]
    model_endpoint: Optional[str] = Field(None, alias="model-endpoint")


class StarpackInput(BaseModel):
    package: Optional[PackageInput]
    deployment: Optional[DeployInput]
