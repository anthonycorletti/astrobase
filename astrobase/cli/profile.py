import json

import typer

from astrobase.cli.config import ASTROBASE_HOST_PORT, AstrobaseConfig, AstrobaseProfile

app = typer.Typer(help="""Manage Astrobase profiles.""")


@app.command()
def create(
    name: str,
    host: str = typer.Option(default="localhost"),
    port: str = typer.Option(default=ASTROBASE_HOST_PORT),
    secure: bool = typer.Option(default=False),
    gcp_creds: str = typer.Option(None),
    aws_creds: str = typer.Option(None),
    aws_profile_name: str = typer.Option(None),
    azure_client_id: str = typer.Option(None),
    azure_client_secret: str = typer.Option(None),
    azure_subscription_id: str = typer.Option(None),
    azure_tenant_id: str = typer.Option(None),
) -> None:
    """Create a profile."""
    astrobase_config = AstrobaseConfig()
    new_profile = AstrobaseProfile(
        name=name,
        host=host,
        port=port,
        secure=secure,
        gcp_creds=gcp_creds,
        aws_creds=aws_creds,
        aws_profile_name=aws_profile_name,
        azure_client_id=azure_client_id,
        azure_client_secret=azure_client_secret,
        azure_subscription_id=azure_subscription_id,
        azure_tenant_id=azure_tenant_id,
    )
    astrobase_config.config[name] = new_profile.dict()
    astrobase_config.write_config(astrobase_config.config)
    typer.echo(f"Created profile {name}.")


@app.command("list")
def _list() -> None:
    """List profile names."""
    astrobase_config = AstrobaseConfig()
    typer.echo(json.dumps(sorted(list(astrobase_config.config.keys())), indent=2))


@app.command("get")
def get(name: str = typer.Argument(...)) -> None:
    """Get one profile."""
    astrobase_config = AstrobaseConfig()
    if name in astrobase_config.config:
        typer.echo(json.dumps((astrobase_config.config[name]), indent=2))
    else:
        typer.echo(f"Profile {name} not found.")


@app.command()
def current() -> None:
    """Retrieve the current profile."""
    astrobase_config = AstrobaseConfig()
    typer.echo(json.dumps((dict(astrobase_config.current_profile())), indent=2))


@app.command()
def delete(name: str = typer.Argument(...)) -> None:
    """Delete a profile."""
    astrobase_config = AstrobaseConfig()
    typer.confirm(f"Are you sure you want to delete the {name} profile?")
    if name in astrobase_config.config:
        del astrobase_config.config[name]
        astrobase_config.write_config(astrobase_config.config)
        typer.echo(f"Deleted {name} profile.")
    else:
        typer.echo(f"Profile {name} not found.")
