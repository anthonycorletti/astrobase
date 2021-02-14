from pydantic import BaseModel


class AstroToken(BaseModel):
    token: str
    token_type: str
