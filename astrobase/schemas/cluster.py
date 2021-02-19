from typing import Optional

from pydantic import BaseModel, Field, validator

from astrobase.helpers.name import random_name


class GoogleClusterBase(BaseModel):
    name: Optional[str] = Field(default_factory=random_name)
    zone: str
    project_id: str
    initial_node_count: int = 1

    @validator("name")
    def name_is_set(cls, name: str) -> str:
        if not name:
            return random_name()
        return name


class GoogleClusterCreate(GoogleClusterBase):
    pass


class GoogleClusterUpdate(GoogleClusterBase):
    pass


class GoogleCluster(GoogleClusterBase):
    pass


class GoogleClusterCreateAPIFilter(BaseModel):
    name: str
    initial_node_count: str


class GoogleClusterUpdateAPIFilter(BaseModel):
    pass
