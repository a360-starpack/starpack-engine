from typing import Any, Dict
from yaml import load, Loader
from fastapi import HTTPException

from .._config import settings
from ..resources.plugins import Plugin


class PluginEngine:
    plugins: Dict[str, Plugin] = dict()

    @classmethod
    def _discover(cls):
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
                plugin_information = load(config_yaml, Loader=Loader)

            # Add the folder name for dynamic loading later
            plugin_information["folder"] = plugin_path.name

            # Parse the object into our Pydantic model for type validation
            plugin_data = Plugin.parse_obj(plugin_information)

            # Add the plugin's data to our list of plugins
            cls.plugins[plugin_data.name] = plugin_data

    @classmethod
    def _load(cls):
        """
        Load all plugins into memory and install requirements.
        """
        for name, plugin in cls.plugins.items():
            print(f"Loading in plugin: {name}")
            plugin.install_dependencies()
            plugin.load_method()

    @classmethod
    def invoke(cls, plugin: str) -> Any:
        try:
            return cls.plugins[plugin].invoke()
        except KeyError:
            raise HTTPException(
                status_code=404, detail=f"The plugin, `{plugin}`, was not found"
            )
