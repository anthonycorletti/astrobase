import typer

from astrobasecloud.providers.main import AstrobaseGCPClient
from astrobasecloud.types.gcp import GCPSetupSpec

app = typer.Typer(help="""Configure a cloud provider with Astrobase.""")


@app.command("gcp", help="""Configure Google Cloud Platform with Astrobase.""")
def _gcp(
    project_id: str = typer.Option(
        ...,
        "--project-id",
        help="GCP Project ID that Astrobase will use for setup.",
    ),
    service_name: str = typer.Option(
        ...,
        "--service-name",
        help="GCP Service Name Identifier that Astrobase "
        "will enable (e.g. 'container.googleapis.com').",
    ),
) -> None:
    ab_client = AstrobaseGCPClient()
    setup_spec = GCPSetupSpec(project_id=project_id, service_name=service_name)
    ab_client.setup_provider(setup_spec=GCPSetupSpec(**setup_spec.dict()))
