import typer
import uvicorn

from astrobasecloud import __version__
from astrobasecloud.cli import cluster, profile, provider
from astrobasecloud.server.config import AstrobaseServerConfig

name = f"Astrobase {__version__}"

app = typer.Typer(name=name, no_args_is_help=True)
app.add_typer(profile.app, name="profile", no_args_is_help=True)
app.add_typer(cluster.app, name="cluster", no_args_is_help=True)
app.add_typer(provider.app, name="provider", no_args_is_help=True)


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
    from astrobasecloud.server.main import api

    astrobase_server_config = AstrobaseServerConfig()
    uvicorn.run(
        api,
        port=astrobase_server_config.port,
        host=astrobase_server_config.host,
    )
