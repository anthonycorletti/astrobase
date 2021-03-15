from enum import Enum, unique
from typing import List, Optional

from pydantic import BaseModel, Field, validator

from astrobase.helpers.name import random_name


@unique
class ReleaseChannel(str, Enum):
    regular = "REGULAR"
    rapid = "RAPID"


class GKEReleaseChannel(BaseModel):
    channel: ReleaseChannel = ReleaseChannel.regular


class GKEAutoscaling(BaseModel):
    enabled: bool = True
    minNodeCount: int = 1
    maxNodeCount: int = 3


class GKEManagement(BaseModel):
    autoUpgrade: bool = True
    autoRepair: bool = True


class GKEUpgradeSettings(BaseModel):
    maxSurge: int = 1


class GKEShieldedInstanceConfig(BaseModel):
    enableIntegrityMonitoring: bool = True


class GKENodePoolConfig(BaseModel):
    machineType: str = "e2-medium"
    diskSizeGb: int = 100
    imageType: str = "COS"
    diskType: str = "pd-ssd"
    shieldedInstanceConfig: GKEShieldedInstanceConfig = GKEShieldedInstanceConfig()
    oauthScopes: List[str] = [
        "https://www.googleapis.com/auth/devstorage.read_only",
        "https://www.googleapis.com/auth/logging.write",
        "https://www.googleapis.com/auth/monitoring",
        "https://www.googleapis.com/auth/servicecontrol",
        "https://www.googleapis.com/auth/service.management.readonly",
        "https://www.googleapis.com/auth/trace.append",
    ]


class GKENodePool(BaseModel):
    name: str
    initialNodeCount: int
    config: GKENodePoolConfig = GKENodePoolConfig()
    autoscaling: GKEAutoscaling = GKEAutoscaling()
    management: GKEManagement = GKEManagement()
    upgradeSettings: GKEUpgradeSettings = GKEUpgradeSettings()


class GKEBase(BaseModel):
    name: Optional[str] = Field(default_factory=random_name)
    location: str
    project_id: str
    parent: Optional[str]
    nodePools: List[GKENodePool]
    releaseChannel: GKEReleaseChannel = GKEReleaseChannel()

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


class GKECreateAPIFilter(BaseModel):
    name: str
    location: str
    nodePools: List[GKENodePool]
    releaseChannel: GKEReleaseChannel


class GKECreateAPI(BaseModel):
    cluster: GKECreateAPIFilter
