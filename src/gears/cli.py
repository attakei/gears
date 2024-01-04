"""CLI entrypoint."""
import logging
import os
from dataclasses import dataclass
from pathlib import Path

import click

from . import core

CONTEXT_SETTINGS = {
    "help_option_names": ["-h", "--help"],
}
Logger = logging.getLogger(__name__)


@dataclass
class CLIEnvironment:
    """Context manager for CLI commands."""

    root: core.RootDirectory


def resolve_root(*args) -> Path:
    """Find target default root path."""
    if args:
        return Path(args[0])
    if "GEARS_ROOT" in os.environ:
        return Path(os.environ["GEARS_ROOT"]).resolve()
    return Path.home() / ".gears"


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option(
    "--root",
    default=resolve_root,
    type=click.Path(path_type=Path, dir_okay=True, file_okay=False),
)
@click.pass_context
def app(ctx: click.Context, root: Path | None):  # noqa: D103
    root_path = resolve_root(root)
    Logger.info(f"Root is {root_path}")
    ctx.obj = CLIEnvironment(root=core.RootDirectory(root_path))


@app.command()
@click.pass_obj
def init(env: CLIEnvironment):
    """Initialize root-directory."""
    click.echo(click.style("This is not implemented!!", fg="red"))


def main():
    """Entrypoint."""
    app()
