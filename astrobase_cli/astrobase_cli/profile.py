import os
from typing import Optional

import typer

from utils.config import AstrobaseConfig
from utils.formatter import json_out

app = typer.Typer(help="""Manage Astrobase profiles across environments.""")
astrobase_config = AstrobaseConfig()


@app.command()
def create(
    name: str,
    api_key: str = typer.Option(None),
    server: str = typer.Option(default="http://localhost:8787"),
):
    astrobase_config.config_dict[name] = {"server": server, "api_key": api_key}
    astrobase_config.write_config(astrobase_config.config_dict)
    typer.echo(f"Created profile {name}.")


@app.command()
def get(name: Optional[str] = None):
    if name is not None:
        if name in astrobase_config.config_dict:
            typer.echo(json_out(astrobase_config.config_dict[name]))
    else:
        typer.echo(json_out(astrobase_config.config_dict))


@app.command()
def current():
    profile_env = os.getenv(astrobase_config.ASTROBASE_PROFILE, "profile not set!!")
    profile = typer.style(profile_env, fg=typer.colors.WHITE, bold=True)
    typer.echo(f"Current Astrobase profile: {profile}")
    if astrobase_config.current_profile:
        typer.echo(json_out(astrobase_config.current_profile))


@app.command()
def delete(name: str):
    typer.confirm(f"Are you sure you want to delete the {name} profile?")
    if name in astrobase_config.config_dict:
        del astrobase_config.config_dict[name]
        astrobase_config.write_config(astrobase_config.config_dict)
        typer.echo(f"Deleted {name} profile.")
    else:
        typer.echo(f"Profile {name} not found.")
