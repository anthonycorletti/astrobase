import json


def json_out(d: dict) -> str:
    return json.dumps(d, indent=2)
