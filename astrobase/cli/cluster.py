import typer
import yaml

from astrobase.providers.main import AstrobaseClient

app = typer.Typer(help="""Manage Kubernetes Clusters.""")


@app.command("create")
def _create(
    spec_filepath: str = typer.Option(
        ..., "--file", "-f", help="Path to an Astrobase cluster spec."
    )
) -> None:
    """Create one or many Kubernetes clusters."""
    ab_client = AstrobaseClient()
    with open(spec_filepath, "r") as spec_file:
        spec_data = yaml.safe_load_all(spec_file)
        for spec in spec_data:
            for cluster_spec in spec["clusters"]:
                ab_client.create_cluster(
                    provider=cluster_spec["provider"],
                    cluster_spec=cluster_spec,
                )


@app.command("delete")
def _delete(
    spec_filepath: str = typer.Option(
        "--file", "-f", help="Path to an Astrobase cluster spec."
    )
) -> None:
    """Delete one or many Kubernetes clusters."""
    ab_client = AstrobaseClient()
    with open(spec_filepath, "r") as spec_file:
        spec_data = yaml.safe_load_all(spec_file)
        for spec in spec_data:
            for cluster_spec in spec["clusters"]:
                ab_client.delete_cluster(
                    provider=cluster_spec["provider"],
                    cluster_spec=cluster_spec,
                )
