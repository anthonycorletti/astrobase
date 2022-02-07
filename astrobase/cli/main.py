import typer
import uvicorn

from astrobase import __version__
from astrobase.cli import cluster, iam, profile
from astrobase.cli.config import AstrobaseConfig

name = f"Astrobase {__version__}"

app = typer.Typer(name=name, no_args_is_help=True)
app.add_typer(profile.app, name="profile", no_args_is_help=True)
app.add_typer(cluster.app, name="cluster", no_args_is_help=True)
app.add_typer(iam.app, name="iam", no_args_is_help=True)


@app.callback()
def main_callback() -> None:
    pass


main_callback.__doc__ = name


@app.command("version")
def _version() -> None:
    """Print the Astrobase CLI version."""
    typer.echo(__version__)


@app.command("server")
def _server() -> None:
    """Start the Astrobase server."""
    from astrobase.server.main import api

    astrobase_config = AstrobaseConfig()
    uvicorn.run(
        api,
        port=astrobase_config.current_profile.port,
        host=astrobase_config.current_profile.host,
    )
