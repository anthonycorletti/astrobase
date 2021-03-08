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
    google_application_credentials: str = typer.Option(None),
    aws_credentials: str = typer.Option(None),
    aws_profile_name: str = typer.Option(None),
):
    astrobase_config.config_dict[name] = {
        "server": server,
        "api_key": api_key,
        "google_application_credentials": google_application_credentials,
        "aws_credentials": aws_credentials,
        "aws_profile_name": aws_profile_name,
    }
    astrobase_config.write_config(astrobase_config.config_dict)
    typer.echo(f"Created profile {name}.")


@app.command("list")
def _list(name: Optional[str] = None):
    if name is not None:
        if name in astrobase_config.config_dict:
            typer.echo(json_out(astrobase_config.config_dict[name]))
    else:
        typer.echo(json_out(astrobase_config.config_dict))


@app.command()
def current():
    if astrobase_config.current_profile:
        typer.echo(
            json_out(
                {
                    os.getenv(
                        astrobase_config.ASTROBASE_PROFILE
                    ): astrobase_config.current_profile
                }
            )
        )
    else:
        typer.echo(
            "no profile is set! set a profile with: export "
            f"{astrobase_config.ASTROBASE_PROFILE}=<my-profile-name>"
        )


@app.command()
def delete(name: str):
    typer.confirm(f"Are you sure you want to delete the {name} profile?")
    if name in astrobase_config.config_dict:
        del astrobase_config.config_dict[name]
        astrobase_config.write_config(astrobase_config.config_dict)
        typer.echo(f"Deleted {name} profile.")
    else:
        typer.echo(f"Profile {name} not found.")
