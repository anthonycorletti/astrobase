from datetime import datetime
from enum import Enum, unique
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, validator

from astrobase.helpers.name import NameHelper


@unique
class CloudProvider(str, Enum):
    amazon = "amazon"
    google = "google"


class ClusterBase(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: Optional[str]
    provider: CloudProvider
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    @validator("name")
    def name_is_set(cls, name: str) -> str:
        if not name:
            n = NameHelper()
            return n.random_name()
        return name


class ClusterCreate(ClusterBase):
    pass


class ClusterUpdate(ClusterBase):
    pass


class Cluster(ClusterBase):
    pass
