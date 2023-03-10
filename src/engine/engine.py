import abc
from typing import Any, Dict, Callable, Optional

from yaml import safe_load

from ._config import settings
from .schemas.plugins import (
    PluginData,
    PluginModel,
    BasicPluginModel,
    ManagementPluginModel,
)

import subprocess
import sys
from importlib import import_module

from .errors import *


class Plugin(abc.ABC):
    data: PluginModel

    def install_dependencies(self) -> None:
        """
        Installs all depedencies for a given Plugin
        """
        if not self.data.dependencies:
            return

        for dependency in self.data.dependencies:
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

    @abc.abstractmethod
    def invoke(self, input_data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        ...


class BasicPlugin(Plugin):
    def __init__(self, data: BasicPluginModel):
        self.data: BasicPluginModel = data

        # import module and get its function
        module = import_module(
            f"..plugins.{self.data.folder}.{self.data.module_name}", package=__name__
        )

        self.function: Callable = getattr(module, self.data.entrypoint)

    def invoke(self, input_data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        if self.data.dataflow:
            plugin_input = {
                key: input_data.get(key) for key in self.data.dataflow.input
            }
        else:
            plugin_input = dict()
        if self.function is None:
            raise UnloadedPluginError()

        output = self.function(**plugin_input)

        input_data.update(output)

        return input_data


class ManagementPlugin(Plugin):
    def __init__(self, data: ManagementPluginModel):
        self.data = data

        # import module and get its function
        self.module = import_module(
            f"..plugins.{self.data.folder}.{self.data.module_name}", package=__name__
        )

    def invoke(self, input_data: Dict[str, Any], **kwargs) -> Dict[str, Any]:

        method = kwargs.get("method")

        if not method:
            raise HTTPException(
                500,
                detail=f"A management-style plugin was invoke without a method to reference.",
            )

        function = getattr(self.module, self.data.entrypoint.__dict__[method])

        if function is None:
            raise UnloadedPluginError()

        output = function(**input_data)

        return output


class PluginEngine:
    plugins: Dict[str, Plugin] = dict()

    @classmethod
    def discover(cls):
        """
        Discover all plugins in our plugin directories.
        """

        # Grab all paths within our internal plugin directory that are directories
        possible_plugins = [
            path for path in settings.internal_plugin_dir.iterdir() if path.is_dir()
        ]

        for plugin_path in possible_plugins:
            # Check if there's a plugin.yaml
            config_path = plugin_path / "plugin.yaml"
            if not config_path.is_file():
                continue

            # Load yaml into memory as Python dict
            with open(config_path) as config_yaml:
                plugin_information = safe_load(config_yaml)

            # Add the folder name for dynamic loading later
            plugin_information["folder"] = plugin_path.name

            # Parse the object into our Pydantic model for type validation
            plugin_data = PluginData.parse_obj(plugin_information).__root__

            if isinstance(plugin_data, BasicPluginModel):
                plugin = BasicPlugin(plugin_data)
            elif isinstance(plugin_data, ManagementPluginModel):
                plugin = ManagementPlugin(plugin_data)
            else:
                raise ValueError()

            # Add the plugin's data to our list of plugins
            cls.plugins[plugin_data.name] = plugin

    @classmethod
    def load(cls):
        """
        Load all plugins into memory and install requirements.
        """
        for name, plugin in cls.plugins.items():
            print(f"Loading in plugin: {name}")
            plugin.install_dependencies()

    @classmethod
    def invoke(
        cls, plugin: str, input_data: Dict[str, Any], method: Optional[str] = None
    ) -> Any:
        try:
            return cls.plugins[plugin].invoke(input_data, method=method)
        except KeyError:
            raise HTTPException(
                status_code=404, detail=f"The plugin, `{plugin}`, was not found"
            )
