from typing import Any, List, Dict
from yaml import load, Loader

from .._config import settings
from ..resources.plugins import Plugin


class PluginEngine:
    plugins: Dict[str, Plugin] = dict()

    def _discover(self):
        """
        Discover all plugins in our plugin directories.
        """
        possible_plugins = [
            path for path in settings.internal_plugin_dir.iterdir() if path.is_dir()
        ]

        for path in possible_plugins:
            config_path = path / "plugin.yaml"
            if not config_path.is_file():
                continue

            with open(config_path) as config_yaml:
                plugin_information = load(config_yaml, Loader=Loader)

            plugin_data = Plugin.parse_obj(plugin_information)

            self.plugins[plugin_data.name] = plugin_data

    def _load(self):
        """
        Load all plugins into memory and install requirements.
        """
        for name, plugin in self.plugins.items():
            print(f"Loading in plugin: {name}")
            plugin.install_dependencies()

    def invoke(self, plugin: str) -> Any:
        return self.plugins[plugin].invoke()
