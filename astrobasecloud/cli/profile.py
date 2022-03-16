import json

import typer

from astrobasecloud.cli.config import (
    ASTROBASE_HOST_PORT,
    AstrobaseCLIConfig,
    AstrobaseProfile,
)

app = typer.Typer(help="""Manage Astrobase profiles.""")


@app.command()
def create(
    name: str,
    host: str = typer.Option(default="localhost"),
    port: str = typer.Option(default=ASTROBASE_HOST_PORT),
    secure: bool = typer.Option(default=True),
) -> None:
    """Create a profile."""
    astrobase_config = AstrobaseCLIConfig()
    new_profile = AstrobaseProfile(name=name, host=host, port=port, secure=secure)
    if name in astrobase_config.config:
        typer.echo(f"Name {name} already present in config. Please try another name!")
        raise typer.Exit(1)
    astrobase_config.config[name] = new_profile.dict()
    astrobase_config.write_config(astrobase_config.config)
    typer.echo(f"Created profile {name}.")


@app.command("get")
def get(name: str = typer.Argument(default=None)) -> None:
    """Get one or many profiles."""
    astrobase_config = AstrobaseCLIConfig()
    if name is None:
        typer.echo(json.dumps(sorted(list(astrobase_config.config.keys())), indent=2))
    else:
        if name in astrobase_config.config:
            typer.echo(json.dumps((astrobase_config.config[name]), indent=2))
        else:
            typer.echo(f"Profile {name} not found.")


@app.command()
def current() -> None:
    """Retrieve the current profile."""
    astrobase_config = AstrobaseCLIConfig()
    typer.echo(json.dumps((dict(astrobase_config.current_profile())), indent=2))


@app.command()
def delete(name: str = typer.Argument(...)) -> None:
    """Delete a profile."""
    astrobase_config = AstrobaseCLIConfig()
    typer.confirm(f"Are you sure you want to delete the {name} profile?")
    if name in astrobase_config.config:
        del astrobase_config.config[name]
        astrobase_config.write_config(astrobase_config.config)
        typer.echo(f"Deleted {name} profile.")
    else:
        typer.echo(f"Profile {name} not found.")
