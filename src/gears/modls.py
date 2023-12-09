"""Core of GEARS."""
from typing import Literal

from pydantic import BaseModel, Field, HttpUrl

ARCHIVE_TYPE = Literal["zip"]


class Gear(BaseModel):
    """'Gear' is item defined installation information.

    This is independent for target (OS and CPU).
    """

    name: str
    version: str
    description: str
    targets: dict[str, "GearTarget"] = Field(default_factory=dict)


class GearTarget(BaseModel):
    """installation information for target machine.

    It can refer that what file should download and what files extract.
    """

    gear: Gear
    os: str
    cpu: str
    url: HttpUrl
    archive: ARCHIVE_TYPE
    paths: list[str] = Field(default_factory=list)
