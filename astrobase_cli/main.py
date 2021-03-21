import docker
import typer
import yaml

from astrobase_cli import __version__ as version
from astrobase_cli import apply, destroy, profile
from schemas.cluster import Clusters
from schemas.resource import ResourceList
from schemas.workflow import Workflows
from utils.config import AstrobaseConfig, AstrobaseDockerConfig
from utils.params import YamlParams

astrobase_apply = apply.Apply()
astrobase_destroy = destroy.Destroy()
docker_client = docker.from_env()
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
    astrobase_config = AstrobaseConfig()
    typer.echo("Initializing Astrobase ... ")
    if not astrobase_config.current_profile:
        typer.echo(
            "No profile is set! set a profile with: export "
            f"{astrobase_config.ASTROBASE_PROFILE}=<my-profile-name>"
        )
        return
    astrobase_docker_config = AstrobaseDockerConfig(
        container_version=astrobase_container_version,
        astrobase_config=astrobase_config,
    )
    typer.echo("Starting Astrobase server ... ")
    docker_client.containers.run(
        image=astrobase_docker_config.image,
        ports=astrobase_docker_config.ports,
        environment=astrobase_docker_config.environment,
        volumes=astrobase_docker_config.volumes,
        auto_remove=astrobase_docker_config.auto_remove,
        detach=astrobase_docker_config.detach,
        name=astrobase_docker_config.name,
    )
    typer.echo(
        "Astrobase initialized and running at "
        f"{astrobase_config.current_profile.server}"
    )


@app.command()
def apply(
    astrobase_yaml_path: str = typer.Option(..., "-f"),
    yaml_params: str = typer.Option(
        None,
        "-v",
        help="Parameters to pass into your yaml. "
        "Format: key=value<space>key2=value2<space>key3=value3<space>...",
    ),
):
    """
    Apply clusters, resources, and workflows.
    """
    params = YamlParams(params=yaml_params)

    with open(astrobase_yaml_path, "r") as f:
        data = yaml.safe_load(f)
        data = params.update_data_with_values(str(data))
        clusters = Clusters(**data)
        resources = ResourceList(**data)
        workflows = Workflows(**data)
        astrobase_apply.apply_clusters(clusters.clusters)
        astrobase_apply.apply_resources(resources.resources)
        astrobase_apply.apply_workflows(workflows.workflows)


@app.command()
def destroy(
    astrobase_yaml_path: str = typer.Option(..., "-f"),
    yaml_params: str = typer.Option(
        None,
        "-v",
        help="Parameters to pass into your yaml."
        "Format: key=value<space>key2=value2<space>key3=value3<space>...",
    ),
):
    """
    Destroy clusters, resources, and workflows.
    """
    params = YamlParams(params=yaml_params)

    with open(astrobase_yaml_path, "r") as f:
        data = yaml.safe_load(f)
        data = params.update_data_with_values(str(data))
        clusters = Clusters(**data)
        resources = ResourceList(**data)
        workflows = Workflows(**data)
        astrobase_destroy.destroy_clusters(clusters.clusters)
        astrobase_destroy.destroy_resources(resources.resources)
        astrobase_destroy.destroy_workflows(workflows.workflows)


if __name__ == "__main__":
    app()
