from typing import Optional

from pydantic import BaseModel, Field, validator

from astrobase.helpers.name import random_name


class GoogleKubernetesClusterBase(BaseModel):
    name: Optional[str] = Field(default_factory=random_name)
    zone: str
    project_id: str
    initial_node_count: int = 1

    @validator("name")
    def name_is_set(cls, name: str) -> str:
        if not name:
            return random_name(component="cluster")
        return name


class GoogleKubernetesClusterCreate(GoogleKubernetesClusterBase):
    pass


class GoogleKubernetesClusterUpdate(GoogleKubernetesClusterBase):
    pass


class GoogleKubernetesCluster(GoogleKubernetesClusterBase):
    pass


class GoogleKubernetesClusterCreateAPIFilter(BaseModel):
    name: str
    initial_node_count: str


class GoogleKubernetesClusterUpdateAPIFilter(BaseModel):
    pass


class AmazonKubernetesClusterBase(BaseModel):
    name: Optional[str] = Field(default_factory=random_name)

    @validator("name")
    def name_is_set(cls, name: str) -> str:
        if not name:
            return random_name()
        return name


class AmazonKubernetesClusterCreate(AmazonKubernetesClusterBase):
    pass


class AmazonKubernetesClusterUpdate(AmazonKubernetesClusterBase):
    pass


class AmazonKubernetesCluster(AmazonKubernetesClusterBase):
    pass


class AmazonKubernetesClusterCreateAPIFilter(BaseModel):
    pass


class AmazonKubernetesClusterUpdateAPIFilter(BaseModel):
    pass
