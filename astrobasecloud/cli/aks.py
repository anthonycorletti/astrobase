import typer
import yaml

from astrobasecloud.providers.main import AstrobaseAzureClient

app = typer.Typer(help="""Manage Azure Kubernetes Engine Clusters.""")


@app.command("create")
def _create(
    resource_group_name: str = typer.Option(...),
    spec_filepath: str = typer.Option(
        ..., "--file", "-f", help="Path to an Astrobase cluster spec."
    ),
) -> None:
    """Create one or many Kubernetes clusters."""
    ab_client = AstrobaseAzureClient()
    with open(spec_filepath, "r") as spec_file:
        spec_data = yaml.safe_load_all(spec_file)
        for spec in spec_data:
            cluster_spec = spec["cluster"]
            cluster_spec["resource_group_name"] = resource_group_name
            ab_client.create_cluster(cluster_spec=cluster_spec)


@app.command("delete")
def _delete(
    resource_group_name: str = typer.Option(...),
    spec_filepath: str = typer.Option(
        ..., "--file", "-f", help="Path to an Astrobase cluster spec."
    ),
) -> None:
    """Delete one or many Kubernetes clusters."""
    ab_client = AstrobaseAzureClient()
    with open(spec_filepath, "r") as spec_file:
        spec_data = yaml.safe_load_all(spec_file)
        for spec in spec_data:
            cluster_spec = spec["cluster"]
            cluster_spec["resource_group_name"] = resource_group_name
            ab_client.delete_cluster(cluster_spec=cluster_spec)
