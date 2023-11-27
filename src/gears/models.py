from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field, HttpUrl


ARCHIVE_TYPE = Literal["zip"]
# TODO: Write all
CPU_TYPE = Literal["x86_64", "aarch64", "AMD64"]
OS_TYPE = Literal["Linux", "Darwin", "Java", "Windows"]


class GearSpec(BaseModel):
    """Spec object for Gear."""
    name: str
    description: str
    version: str

    def __str__(self):
        return f"{self.name}-v{self.version}"


class GearTarget(BaseModel):
    """Gear spec for target(combination of OS and CPU). """
    gear: GearSpec
    os: str
    cpu: str
    url: HttpUrl
    archive: ARCHIVE_TYPE
    paths: list[str] = Field(default_factory=list)

    def __str__(self):
        return f"{self.gear.name}-v{self.gear.version}-{self.os}-{self.cpu}"


class Workspace(BaseModel):
    """Workspace management of Gears."""
    root: Path

    @property
    def bin_dir(self) -> Path:
        return self.root / "bin"

    def init(self):
        self.bin_dir.mkdir(parents=True, exist_ok=True)
