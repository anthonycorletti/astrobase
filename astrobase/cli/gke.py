import typer
import yaml

from astrobase.providers.main import AstrobaseGCPClient

app = typer.Typer(help="""Manage Google Kubernetes Engine Clusters.""")


@app.command("create")
def _create(
    spec_filepath: str = typer.Option(
        ..., "--file", "-f", help="Path to an Astrobase cluster spec."
    )
) -> None:
    """Create one or many Kubernetes clusters."""
    ab_client = AstrobaseGCPClient()
    with open(spec_filepath, "r") as spec_file:
        spec_data = yaml.safe_load_all(spec_file)
        for spec in spec_data:
            for cluster_spec in spec["clusters"]:
                ab_client.create_cluster(cluster_spec=cluster_spec)


@app.command("delete")
def _delete(
    spec_filepath: str = typer.Option(
        "--file", "-f", help="Path to an Astrobase cluster spec."
    )
) -> None:
    """Delete one or many Kubernetes clusters."""
    ab_client = AstrobaseGCPClient()
    with open(spec_filepath, "r") as spec_file:
        spec_data = yaml.safe_load_all(spec_file)
        for spec in spec_data:
            for cluster_spec in spec["clusters"]:
                ab_client.delete_cluster(cluster_spec=cluster_spec)
