"""CLI entrypoint."""
import click

CONTEXT_SETTINGS = {
    "help_option_names": ["-h", "--help"],
}


@click.group(context_settings=CONTEXT_SETTINGS)
def app():  # noqa: D103
    pass


@app.command()
def init():
    """Initialize workspace."""
    click.echo(click.style("This is not implemented!!", fg="red"))


def main():
    """Entrypoint."""
    app()
