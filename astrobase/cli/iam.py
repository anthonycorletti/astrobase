import typer

app = typer.Typer(help="""Manage IAM and Service Accounts.""")


@app.command("create")
def _create() -> None:
    pass


@app.command("get")
def _get() -> None:
    pass


@app.command("delete")
def _delete() -> None:
    pass
