import docker
import typer
import yaml

from astrobase_cli import __version__ as version
from astrobase_cli import profile
from utils.config import AstrobaseConfig
from utils.http import HTTPClient

http_client = HTTPClient()
docker_client = docker.from_env()
astrobase_config = AstrobaseConfig()
name = f"🚀 Astrobase CLI {version} 🧑‍🚀"
app = typer.Typer(name=name)

app.add_typer(profile.app, name="profile")


@app.callback()
def main_callback():
    pass


main_callback.__doc__ = name


@app.command()
def version():
    """
    Print the Astrobase CLI version.
    """
    typer.echo(name)


@app.command()
def init(astrobase_version: str = "latest"):
    """
    Initialize Astrobase.
    """
    typer.echo("Initializing Astrobase ... ")
    typer.echo("Starting Astrobase server ... ")
    google_creds_host = astrobase_config.current_profile.get(
        "google_application_credentials"
    )
    google_creds_container = "/google-credentials.json"
    aws_creds_host = astrobase_config.current_profile.get("aws_credentials")
    aws_creds_container = "/aws-credentials"
    docker_client.containers.run(
        f"astrobase/astrobase:{astrobase_version}",
        ports={"8787/tcp": "8787"},
        environment={
            "GOOGLE_APPLICATION_CREDENTIALS": "/google-credentials.json",
        },
        volumes={
            google_creds_host: {"bind": google_creds_container, "mode": "ro"},
            aws_creds_host: {"bind": aws_creds_container, "mode": "ro"},
        },
        auto_remove=True,
        detach=True,
    )
    typer.echo("Astrobase initialized")


@app.command()
def apply(astrobase_yaml_path: str):
    """
    Apply changes to clusters, services, and workflows.
    """
    with open(astrobase_yaml_path, "r") as f:
        data = yaml.safe_load(f)
        server = f"{astrobase_config.current_profile.get('server')}/gke"
        for cluster in data.get("astrobase").get("clusters"):
            http_client.post(server, cluster)


@app.command()
def destroy(astrobase_yaml_path: str):
    """
    Destroy changes to clusters, services, and workflows.
    """
    typer.echo(f"Destroy the things at {astrobase_yaml_path}!")


@app.command()
def state():
    """
    View state across clusters, services, and workflows.
    """
    typer.echo("Pretty!")


@app.command("import")
def _import():
    """
    Import resources not created by astrobase.
    """
    typer.echo("Wahoo!")


if __name__ == "__main__":
    app()
