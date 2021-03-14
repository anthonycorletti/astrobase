def param_str(params: dict) -> str:
    return "&".join([f"{k}={v}" for k, v in params.items()])
