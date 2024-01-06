"""Settings classes."""
import tomllib
from pathlib import Path

from jinja2 import Template
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings


class RepositorySettings(BaseModel):
    """Settings data of items repository."""

    type: str
    """Type of repository content."""


class Settings(BaseSettings):
    """Root settings object."""

    repos: dict[str, RepositorySettings] = Field(default_factory=dict)
    """Registered repositories."""

    @classmethod
    def load(cls, settings_path: Path) -> "Settings":
        """Read settings textfile and create object."""
        data = tomllib.loads(settings_path.read_text())
        return cls(**data)


def initialize_settings(dist: Path):
    """Output settings-file for initialized user."""
    templates_dir = Path(__file__).parent / "templates"
    context = {}
    template = Template((templates_dir / "settings.toml.j2").read_text())
    dist.write_text(template.render(**context))
