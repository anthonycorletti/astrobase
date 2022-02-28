import multiprocessing
import time

from typer.testing import CliRunner

from astrobase.cli.main import app


def test_cli_start_server(astrobase_cli_runner: CliRunner) -> None:
    p = multiprocessing.Process(
        target=astrobase_cli_runner.invoke, args=(app, ["server"])  # type: ignore
    )
    p.start()
    time.sleep(2)
    p.terminate()
