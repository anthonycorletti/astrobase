import docker
import typer
import yaml

from astrobase_cli import __version__ as version
from astrobase_cli import profile
from astrobase_cli.kubernetes import KubernetesClient
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
def apply(astrobase_yaml_path: str = typer.Option(..., "--files", "-f")):
    """
    Apply changes to clusters, resources, and workflows.
    """
    server = astrobase_config.current_profile.get("server")
    with open(astrobase_yaml_path, "r") as f:
        data = yaml.safe_load(f)

        clusters = data.get("clusters") or []
        for cluster in clusters:
            provider = cluster.get("provider")
            typer.echo(f"Creating {provider} cluster {cluster.get('name')} ... ")
            http_client.post(f"{server}/{provider}", cluster)

        resources = data.get("resources") or []
        for resource in resources:
            provider = resource.get("provider")
            cluster_name = resource.get("cluster_name")
            cluster_location = resource.get("cluster_location")

            kubernetes_client = KubernetesClient()
            if provider == "eks":
                kubernetes_client.apply_eks_kubernetes_resources(
                    kubernetes_resource_dir=resource.get("resource_dir"),
                    cluster_name=cluster_name,
                    cluster_location=cluster_location,
                )
            elif provider == "gke":
                kubernetes_client.apply_gke_kubernetes_resources(
                    kubernetes_resource_dir=resource.get("resource_dir"),
                    cluster_name=cluster_name,
                    cluster_location=cluster_location,
                )
            else:
                typer.echo(f"unsupported provider {provider}")

        workflows = data.get("workflows") or []
        for workflow in workflows:
            typer.echo(f"Applying workflow {workflow.get('name')} ... ")


@app.command()
def destroy(astrobase_yaml_path: str = typer.Option(..., "--files", "-f")):
    """
    Destroy sclusters, resources, and workflows.
    """
    server = astrobase_config.current_profile.get("server")
    with open(astrobase_yaml_path, "r") as f:
        data = yaml.safe_load(f)

        clusters = data.get("clusters") or []
        for cluster in clusters:
            provider = cluster.get("provider")
            cluster_name = cluster.get("name")
            typer.echo(f"Destroying {provider} cluster {cluster.get('name')} ... ")
            if provider == "eks":
                region = cluster.get("region")
                http_client.delete(
                    f"{server}/{provider}/{cluster_name}?region={region}"
                )
            elif provider == "gke":
                project_id = cluster.get("project_id")
                location = cluster.get("location")
                http_client.delete(
                    f"{server}/{provider}/{cluster_name}"
                    f"?project_id={project_id}&location={location}"
                )
            else:
                typer.echo(f"unsupported provider:{provider}")


if __name__ == "__main__":
    app()
