"""CLI entrypoint."""
import logging
import os
from pathlib import Path

import click

CONTEXT_SETTINGS = {
    "help_option_names": ["-h", "--help"],
}
Logger = logging.getLogger(__name__)


def resolve_workspace(*args) -> Path:
    """Find target default workspace path."""
    if "GEARS_HOME" in os.environ:
        return Path(os.environ["GEARS_HOME"]).resolve()
    return Path.home() / ".gears"


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option(
    "--workspace",
    default=resolve_workspace,
    type=click.Path(path_type=Path, dir_okay=True, file_okay=False),
)
@click.pass_context
def app(ctx: click.Context, workspace: Path | None):  # noqa: D103
    resolve_workspace(workspace)
    Logger.info(f"Workspace is {workspace}")


@app.command()
def init():
    """Initialize workspace."""
    click.echo(click.style("This is not implemented!!", fg="red"))


def main():
    """Entrypoint."""
    app()
