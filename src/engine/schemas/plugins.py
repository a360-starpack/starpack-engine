from typing import Dict, Optional, List, Union, Literal
from enum import Enum

from pydantic import BaseModel, Field

from typing_extensions import Annotated


class PluginType(str, Enum):
    manage = "manage"
    basic = "basic"
    custom = "custom"


class Dependency(BaseModel):
    name: str
    version: Optional[str]

    def get_version_string(self) -> str:
        if not self.version:
            version = ""
        elif not (">" in self.version or "<" in self.version):
            version = f"=={self.version}"
        else:
            version = self.version
        return f"{self.name.strip()}{version}"


class BasicDataFlow(BaseModel):
    input: Optional[List[str]]
    output: Optional[List[str]]


class PluginOut(BaseModel):
    name: str
    type: str
    version: str
    description: Optional[str]
    folder: str
    module_name: str
    entrypoint: str
    dataflow: Optional[BasicDataFlow]
    dependencies: Optional[List[Dependency]]


class PluginModel(BaseModel):
    name: str
    type: PluginType
    version: str
    description: Optional[str]
    folder: str
    module_name: str
    entrypoint: Union[str, Dict[str, str]]
    dependencies: Optional[List[Dependency]]


class BasicPluginModel(PluginModel):
    type: Literal[PluginType.basic]
    entrypoint: str
    dataflow: Optional[BasicDataFlow]


class ManagementEntrypoint(BaseModel):
    list: str
    delete: str
    logs: Optional[str]


class ManagementPluginModel(PluginModel):
    type: Literal[PluginType.manage]
    entrypoint: ManagementEntrypoint


class PluginData(BaseModel):
    __root__: Annotated[
        Union[BasicPluginModel, ManagementPluginModel], Field(discriminator="type")
    ]
