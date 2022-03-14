import time
from multiprocessing import Process

from typer.testing import CliRunner

from astrobasecloud.cli.main import app


def test_cli_start_server(astrobase_cli_runner: CliRunner) -> None:
    p = Process(
        target=astrobase_cli_runner.invoke, args=(app, ["server"])  # type: ignore
    )
    p.start()
    time.sleep(2)
    p.terminate()
