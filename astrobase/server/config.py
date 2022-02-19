from pydantic import BaseModel, StrictInt, StrictStr


class AstrobaseServerConfig(BaseModel):
    host: StrictStr = "localhost"
    port: StrictInt = 8787
