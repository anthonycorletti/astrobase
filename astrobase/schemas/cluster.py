from enum import Enum, unique
from typing import Optional

from pydantic import UUID4, BaseModel, validator

from astrobase.helpers.name import NameHelper


@unique
class CloudPlatform(str, Enum):
    amazon = "amazon"
    google = "google"


class ClusterBase(BaseModel):
    name: Optional[str]
    cloud_platform: CloudPlatform

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
    id: UUID4
