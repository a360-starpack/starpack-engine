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


class Plugin(BaseModel):
    name: str
    version: str
    description: Optional[str]
    module_name: str = Field(..., alias="module-name")
    entrypoint: str
    dependencies: Optional[List[Dependency]]
    function: Optional[Callable]

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

    def invoke(self) -> None:
        print(f"engine.plugins.{self.name}.{self.module_name}")
        module = import_module(f"engine.plugins.{self.name}.{self.module_name}")
        infer_func = getattr(module, self.entrypoint)

        return infer_func()
