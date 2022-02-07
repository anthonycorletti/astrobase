from typing import Dict


def query_str(params: Dict) -> str:
    return "&".join([f"{k}={v}" for k, v in params.items()])
