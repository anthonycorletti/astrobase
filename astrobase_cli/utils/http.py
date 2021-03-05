import json

import requests
import typer

from utils.config import AstrobaseConfig


class HTTPClient:
    def __init__(self):
        self.config = AstrobaseConfig()

    def post(self, url: str, data: dict) -> None:
        res = requests.post(url, json=data)
        data = res.json()
        if res.ok:
            typer.echo(data)
        else:
            typer.echo(f"Request errored with code {res.status_code}:")
            try:
                typer.echo(data)
            except json.decoder.JSONDecodeError:
                typer.echo(res.text)

    def get(self, url: str) -> dict:
        res = requests.get(url)
        data = res.json()
        if data.get("error"):
            typer.echo(data)
            return {}
        if res.ok:
            return data
        else:
            try:
                typer.echo(data)
                return {}
            except json.decoder.JSONDecodeError:
                typer.echo(res.text)
                return {}
