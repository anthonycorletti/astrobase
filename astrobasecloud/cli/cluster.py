import typer

from astrobasecloud.cli import aks, eks, gke

app = typer.Typer(help="""Manage Kubernetes Clusters.""")
app.add_typer(gke.app, name="gke", no_args_is_help=True)
app.add_typer(eks.app, name="eks", no_args_is_help=True)
app.add_typer(aks.app, name="aks", no_args_is_help=True)
