from typing import List, Optional

from pydantic import BaseModel, validator


class X(BaseModel):
    name: Optional[str]


class Y(BaseModel):
    name: str
    xs: List[X]

    @validator("xs", pre=True, always=True)
    def set_xs_names(cls, v, values):
        for x in v:
            if not x.name:
                x.name = values["name"]
        return v
