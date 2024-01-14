"""Domain models for package management.

These are used in program core layer.
"""
import functools
from typing import Literal

from pydantic import BaseModel, Field

from . import __doc__, __version__

CPU_STRING = Literal["x64"]
OS_STRING = Literal["windows", "macos", "linux"]


class GearTarget(BaseModel):
    """Installation information for OS and CPU-architecture."""

    name: str
    os: OS_STRING
    cpu: CPU_STRING
    url: str
    file_type: str
    paths: list[str] = Field(default_factory=list)
    """Items to install from downloaded file."""


class GearSpec(BaseModel):
    """Generic information for installation item."""

    name: str
    description: str
    version: str
    targets: dict[str, GearTarget] = Field(default_factory=dict)
    """Collection of installation target. Key is based from os-string and cpu-string."""

    @property
    def detail_text(self):
        """detail_text for users."""
        lines = [
            f"Name:        {self.name}",
            f"Description: {self.description}",
            f"Version:     {self.version}",
            f"Targets:     {', '.join(self.targets.keys())}",
        ]
        return "\n".join(lines)


@functools.cache
def get_spec_of_itself() -> GearSpec:
    """Return spec object about gear itself (single-exexutable version)."""
    spec = GearSpec(name="gears", description=__doc__, version=__version__)
    spec.targets = {
        f"{os}/x64": GearTarget(
            name="gears",
            os=os,
            cpu="x64",
            url=f"https://github.com/attakei/gears/releases/download/v{__version__}/gears-v{__version__}-{os}_x64.zip",  # noqa
            file_type="zip",
        )
        for os in ["windows", "macos", "linux"]
    }
    for k in spec.targets.keys():
        if k.startswith("windows/"):
            spec.targets[k].paths = ["gears.exe"]
        else:
            spec.targets[k].paths = ["gears"]
    return spec
