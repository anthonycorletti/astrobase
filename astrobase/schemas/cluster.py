from typing import Optional

from pydantic import BaseModel, Field, validator

from astrobase.helpers.name import random_name


class GKEAutopilotEnabled(BaseModel):
    enabled: bool = True


class GKEBase(BaseModel):
    name: Optional[str] = Field(default_factory=random_name)
    location: str
    project_id: str
    parent: Optional[str]
    autopilot: GKEAutopilotEnabled = GKEAutopilotEnabled(enabled=True)

    @validator("name")
    def name_is_set(cls, name: str) -> str:
        if not name:
            return random_name()
        return name

    @validator("parent", pre=True, always=True)
    def set_parent(cls, v, values) -> str:
        if not v:
            return f"projects/{values['project_id']}/locations/{values['location']}"
        return v


class GKECreate(GKEBase):
    pass


class GKE(GKEBase):
    pass


class GKECreateFilter(BaseModel):
    name: str
    location: str
    autopilot: GKEAutopilotEnabled


class GKECreateAPI(BaseModel):
    cluster: GKECreateFilter


class EKSBase(BaseModel):
    """
    todo!!!
    """

    name: Optional[str] = Field(default_factory=random_name)

    @validator("name")
    def name_is_set(cls, name: str) -> str:
        if not name:
            return random_name()
        return name


class EKSCreate(EKSBase):
    """
    todo!!!
    """

    pass


class EKS(EKSBase):
    """
    todo!!!
    """

    pass


class EKSCreateAPIBody(BaseModel):
    """
    todo!!!
    """

    pass
