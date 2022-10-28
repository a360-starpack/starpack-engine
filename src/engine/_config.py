from pathlib import Path

from pydantic import BaseSettings


class Settings(BaseSettings):
    root_path: Path = Path(__file__).parent.resolve()

    @property
    def internal_plugin_dir(self) -> Path:
        return self.root_path / "plugins"

    @property
    def external_plugin_dir(self) -> Path:
        return self.root_path / "external" / "plugins"


settings = Settings()
