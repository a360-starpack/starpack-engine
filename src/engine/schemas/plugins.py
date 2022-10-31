import sys
from pydantic import BaseModel, Field
from typing import Any, Dict, Optional, List, Callable
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


class DataFlow(BaseModel):
    input: Optional[List[str]]
    output: Optional[List[str]]


class Plugin(BaseModel):
    name: str
    version: str
    description: Optional[str]
    folder: str
    module_name: str
    entrypoint: str
    dataflow: Optional[DataFlow]
    dependencies: Optional[List[Dependency]]
    function: Optional[Callable]

    def load_method(self) -> None:
        module = import_module(f"...plugins.{self.folder}.{self.module_name}", package=__name__)
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

    def invoke(self, input_data: Dict[str, Any]) -> None:
        if self.dataflow:
            plugin_input = {key: input_data.get(key) for key in self.dataflow.input}
        else:
            plugin_input = dict()
        if self.function is None:
            raise UnloadedPluginError()

        output = self.function(**plugin_input)

        input_data.update(output)
