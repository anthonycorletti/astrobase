from typing import List

from pydantic import BaseModel


class Resource(BaseModel):
    name: str
    provider: str
    cluster_name: str
    cluster_location: str
    resource_location: str


class ResourceList(BaseModel):
    resources: List[Resource] = []
