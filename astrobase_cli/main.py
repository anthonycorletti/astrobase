import typer

from astrobase_cli import __version__ as version
from astrobase_cli import profile
from utils.config import AstrobaseConfig

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
def plan(astrobase_yaml_path: str):
    """
    Preview changes to clusters, services, and workflows.
    """
    typer.echo(f"Plan the things at {astrobase_yaml_path}!")


@app.command()
def apply(astrobase_yaml_path: str):
    """
    Apply changes to clusters, services, and workflows.
    """
    typer.echo(f"Apply the things at {astrobase_yaml_path}!")


if __name__ == "__main__":
    app()
