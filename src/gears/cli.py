"""CLI entrypoint."""
import logging
import os
from dataclasses import dataclass
from pathlib import Path

import click

from . import core, settings

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
    env = CLIEnvironment(root=core.RootDirectory(root_path))
    ctx.obj = env
    if ctx.invoked_subcommand == "init":
        return
    # If subcommand requires root-directory, verify it before running.
    verified, reason = env.root.verify()
    if not verified:
        click.echo(click.style(reason, fg="red"))
        ctx.exit(1)
    Logger.info(f"Root is {root_path}")


@app.command()
@click.pass_obj
def init(env: CLIEnvironment):
    """Initialize root-directory."""
    if env.root.settings_path.exists():
        click.echo("setting.toml is already exisis in root-directory.")
        click.confirm("Override it?", abort=True)

    env.root.make_dirs()
    settings.initialize_settings(env.root.settings_path)
    click.echo(click.style("Welcome to Gears!!", fg="green"))
    click.echo(
        click.style(
            f"Please add '{env.root.bin_dir.resolve()}' into your PATH environment varibale.",  # noqa: E501
            fg="green",
        )
    )


@app.command()
@click.pass_obj
def info(env: CLIEnvironment):
    """Display workspace information."""
    click.echo(f"Root directory is {env.root}")
    click.echo(f"- {env.root.count_bin()} items are installed")


@app.command()
@click.pass_obj
def self(env: CLIEnvironment):
    """Access information of gears itself."""
    from .models import get_spec_of_itself

    spec = get_spec_of_itself()
    click.echo(spec.detail_text)


def main():
    """Entrypoint."""
    app()
