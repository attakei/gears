"""Core classes for gears."""
from pathlib import Path
from typing import Tuple


class RootDirectory:
    """File structure management for root-directory."""

    def __init__(self, root: Path):
        self._root = root

    def __repr__(self):
        return f"<Root on {self._root}>"

    @property
    def settings_path(self) -> Path:
        """Settings file for Gears's root."""
        return self._root / "settings.toml"

    @property
    def bin_dir(self) -> Path:
        """Directory to save executable files."""
        return self._root / "bin"

    @property
    def repos_dir(self) -> Path:
        """Directory for item repositories."""
        return self._root / "repos"

    @property
    def logs_dir(self) -> Path:
        """Directory of log output."""
        return self._root / "logs"

    def make_dirs(self):
        """Create root-directory with subs.

        This method runs only to create directries, not to delete files.
        """
        self._root.mkdir(exist_ok=True)
        self.bin_dir.mkdir(exist_ok=True)
        self.logs_dir.mkdir(exist_ok=True)

    def verify(self) -> Tuple[bool, str | None]:
        """Check that itself is rightly workspace(filebase)."""
        if not self._root.exists():
            return False, "Root directory is not exists."
        if not self.settings_path.exists():
            return False, "Settings file is not exists in root-directory."
        return True, None
