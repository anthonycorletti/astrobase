import docker
import typer
import yaml

from astrobase_cli import __version__ as version
from astrobase_cli import apply, destroy, profile
from utils.config import AstrobaseConfig

astrobase_apply = apply.Apply()
astrobase_destroy = destroy.Destroy()
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
def init(astrobase_container_version: str = "latest"):
    """
    Initialize Astrobase.
    """
    typer.echo("Initializing Astrobase ... ")
    if not astrobase_config.current_profile:
        typer.echo(
            "no profile is set! set a profile with: export "
            f"{astrobase_config.ASTROBASE_PROFILE}=<my-profile-name>"
        )
        return
    environment, volumes = {}, {}
    google_creds_container = "/google-credentials.json"
    aws_creds_container = "/aws-credentials"
    google_creds_host = astrobase_config.current_profile.get(
        "google_application_credentials"
    )
    if google_creds_host:
        environment["GOOGLE_APPLICATION_CREDENTIALS"] = google_creds_container
        volumes[google_creds_host] = {"bind": google_creds_container, "mode": "ro"}
    aws_creds_host = astrobase_config.current_profile.get("aws_credentials")
    if aws_creds_host:
        volumes[aws_creds_host] = {"bind": aws_creds_container, "mode": "ro"}
    aws_profile_name = astrobase_config.current_profile.get("aws_profile_name")
    if aws_profile_name:
        environment["AWS_SHARED_CREDENTIALS_FILE"] = aws_creds_container
        environment["AWS_PROFILE"] = aws_profile_name
    typer.echo("Starting Astrobase server ... ")
    docker_client.containers.run(
        f"astrobase/astrobase:{astrobase_container_version}",
        ports={"8787/tcp": "8787"},
        environment=environment,
        volumes=volumes,
        auto_remove=True,
        detach=True,
        name=f"astrobase-{astrobase_config.profile_name}",
    )
    typer.echo("Astrobase initialized")


@app.command()
def apply(astrobase_yaml_path: str = typer.Option(..., "-f")):
    """
    Apply clusters, resources, and workflows.
    """
    with open(astrobase_yaml_path, "r") as f:
        data = yaml.safe_load(f)

        clusters = data.get("clusters") or []
        resources = data.get("resources") or []
        workflows = data.get("workflows") or []  # TODO!

        astrobase_apply.apply_clusters(clusters)
        astrobase_apply.apply_resources(resources)
        astrobase_apply.apply_workflows(workflows)


@app.command()
def destroy(astrobase_yaml_path: str = typer.Option(..., "-f")):
    """
    Destroy clusters, resources, and workflows.
    """
    with open(astrobase_yaml_path, "r") as f:
        data = yaml.safe_load(f)

        clusters = data.get("clusters") or []
        resources = data.get("resources") or []
        workflows = data.get("workflows") or []  # TODO!

        astrobase_destroy.destroy_clusters(clusters)
        astrobase_destroy.destroy_resources(resources)
        astrobase_destroy.destroy_workflows(workflows)


if __name__ == "__main__":
    app()
