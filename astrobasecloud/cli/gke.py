import typer
import yaml

from astrobasecloud.providers.main import AstrobaseGCPClient
from astrobasecloud.types.gcp import GKECluster

app = typer.Typer(help="""Manage Kubernetes Clusters.""")


@app.command("create")
def _create(
    project_id: str = typer.Option(...),
    spec_filepath: str = typer.Option(
        ..., "--file", "-f", help="Path to an Astrobase cluster spec."
    ),
) -> None:
    """Create one or many Kubernetes clusters."""
    ab_client = AstrobaseGCPClient()
    with open(spec_filepath, "r") as spec_file:
        spec_data = yaml.safe_load_all(spec_file)
        for spec in spec_data:
            cluster_spec = spec["cluster"]
            cluster_spec["project_id"] = project_id
            ab_client.create_cluster(cluster_spec=GKECluster(**cluster_spec))


@app.command("delete")
def _delete(
    project_id: str = typer.Option(...),
    spec_filepath: str = typer.Option(
        ..., "--file", "-f", help="Path to an Astrobase cluster spec."
    ),
) -> None:
    """Delete one or many Kubernetes clusters."""
    ab_client = AstrobaseGCPClient()
    with open(spec_filepath, "r") as spec_file:
        spec_data = yaml.safe_load_all(spec_file)
        for spec in spec_data:
            cluster_spec = spec["cluster"]
            cluster_spec["project_id"] = project_id
            ab_client.delete_cluster(cluster_spec=GKECluster(**cluster_spec))
