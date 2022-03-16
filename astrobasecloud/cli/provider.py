import typer

from astrobasecloud.cli import setup

app = typer.Typer(help="""Manage Cloud Provider Configurations.""")
app.add_typer(setup.app, name="setup", no_args_is_help=True)
