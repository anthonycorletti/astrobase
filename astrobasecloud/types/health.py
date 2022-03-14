from datetime import datetime

from pydantic import BaseModel


class HealthcheckResponse(BaseModel):
    version: str
    message: str
    time: datetime
