from datetime import datetime
from enum import Enum, unique
from typing import Optional

from pydantic import BaseModel, Field, validator

from astrobase.helpers.name import random_name


@unique
class CloudProvider(str, Enum):
    amazon = "amazon"
    google = "google"


class GoogleClusterBase(BaseModel):
    name: Optional[str] = Field(default_factory=random_name)
    project_id: str
    zone: str
    provider: str = "google"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

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
