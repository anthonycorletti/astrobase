from typing import Optional

from pydantic import BaseModel, Field, validator

from astrobase.helpers.name import random_name


class GKEBase(BaseModel):
    name: Optional[str] = Field(default_factory=random_name)
    zone: str
    project_id: str
    initial_node_count: int = 1

    @validator("name")
    def name_is_set(cls, name: str) -> str:
        if not name:
            return random_name()
        return name


class GKECreate(GKEBase):
    pass


class GKEUpdate(GKEBase):
    pass


class GKE(GKEBase):
    pass


class GKECreateAPIFilter(BaseModel):
    name: str
    initial_node_count: str


class GKEUpdateAPIFilter(BaseModel):
    pass


class EKSBase(BaseModel):
    name: Optional[str] = Field(default_factory=random_name)

    @validator("name")
    def name_is_set(cls, name: str) -> str:
        if not name:
            return random_name()
        return name


class EKSCreate(EKSBase):
    pass


class EKSUpdate(EKSBase):
    pass


class EKS(EKSBase):
    pass


class EKSCreateAPIFilter(BaseModel):
    pass


class EKSUpdateAPIFilter(BaseModel):
    pass
