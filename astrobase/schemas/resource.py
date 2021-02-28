from typing import Optional

from pydantic import BaseModel, Field, validator

from astrobase.helpers.name import random_name


class KubernetesResourceBase(BaseModel):
    name: Optional[str] = Field(default_factory=random_name)
    cluster_name: str
    resource_dir: str

    @validator("name")
    def name_is_set(cls, name: str) -> str:
        if not name:
            return random_name()
        return name


class KubernetesResourceCreate(KubernetesResourceBase):
    pass


class KubernetesResourceUpdate(KubernetesResourceBase):
    pass


class KubernetesResource(KubernetesResourceBase):
    pass
