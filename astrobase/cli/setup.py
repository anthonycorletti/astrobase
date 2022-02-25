import typer

from astrobase.providers.main import AstrobaseGCPClient
from astrobase.types.gcp import GCPSetupSpec

app = typer.Typer(help="""Configure a cloud provider with Astrobase.""")


@app.command("gcp", help="""Configure Google Cloud Platform with Astrobase.""")
def _gcp(
    project_id: str = typer.Option(
        ...,
        "--project-id",
        help="GCP Project ID that Astrobase will use for setup.",
    )
) -> None:
    ab_client = AstrobaseGCPClient()
    setup_spec = GCPSetupSpec(project_id=project_id)
    ab_client.setup_provider(setup_spec=GCPSetupSpec(**setup_spec.dict()))
