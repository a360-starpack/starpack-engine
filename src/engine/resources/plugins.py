import sys
from pydantic import BaseModel, Field
from typing import Optional, List, Callable
import subprocess
from ..errors import *
from importlib import import_module


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


class Argument(BaseModel):
    name: str
    type: Optional[str]


class Resources(BaseModel):
    input: List[Argument]
    output: List[Argument]


class Plugin(BaseModel):
    name: str
    version: str
    description: Optional[str]
    folder: str
    module_name: str = Field(..., alias="module-name")
    entrypoint: str
    dependencies: Optional[List[Dependency]]
    function: Optional[Callable]

    def load_method(self) -> None:
        print(f"engine.plugins.{self.folder}.{self.module_name}")
        module = import_module(f"engine.plugins.{self.folder}.{self.module_name}")
        self.function = getattr(module, self.entrypoint)

    def install_dependencies(self) -> None:
        """
        Installs all depedencies for a given Plugin
        """
        if not self.dependencies:
            return

        for dependency in self.dependencies:
            try:
                subprocess.check_call(
                    [
                        sys.executable,
                        "-m",
                        "pip",
                        "install",
                        dependency.get_version_string(),
                    ]
                )
            except subprocess.CalledProcessError as e:
                print(e)
                raise ImproperRequirementError()

    def invoke(self, *args, **kwargs) -> None:
        if self.function is None:
            raise UnloadedPluginError()

        return self.function(*args, **kwargs)
