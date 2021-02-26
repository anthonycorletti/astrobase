import requests
import typer

from utils.config import AstrobaseConfig


class HTTPClient:
    def __init__(self):
        self.config = AstrobaseConfig()

    def post(self, url: str, data: dict) -> dict:
        res = requests.post(url, json=data)
        if res.ok:
            return dict(res.json())
        else:
            typer.echo(f"Request failed with code {res.status_code}:")
            typer.echo(res.json())
