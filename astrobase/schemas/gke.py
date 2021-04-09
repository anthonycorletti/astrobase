from enum import Enum, unique
from typing import Dict, List, Optional

from pydantic import BaseModel, Field

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


@unique
class AcceleratorType(str, Enum):
    nvidia_tesla_a100 = "nvidia-tesla-a100"
    nvidia_tesla_k80 = "nvidia-tesla-k80"
    nvidia_tesla_p100 = "nvidia-tesla-p100"
    nvidia_tesla_p4 = "nvidia-tesla-p4"
    nvidia_tesla_t4 = "nvidia-tesla-t4"
    nvidia_tesla_v100 = "nvidia-tesla-v100"


class Accelerator(BaseModel):
    acceleratorCount: int = 1
    acceleratorType: AcceleratorType = AcceleratorType.nvidia_tesla_a100


class GKEShieldedInstanceConfig(BaseModel):
    enableIntegrityMonitoring: bool = True


class GKENodePoolConfig(BaseModel):
    machineType: str = "e2-medium"
    diskSizeGb: int = 20
    imageType: str = "COS"
    diskType: str = "pd-ssd"
    accelerators: List[Accelerator] = []
    shieldedInstanceConfig: GKEShieldedInstanceConfig = GKEShieldedInstanceConfig()
    metadata: Optional[Dict[str, str]] = {}
    labels: Optional[Dict[str, str]] = {}
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
    nodePools: List[GKENodePool]
    releaseChannel: GKEReleaseChannel = GKEReleaseChannel()
    resourceLabels: Optional[Dict[str, str]] = {}


class GKECreate(GKEBase):
    pass


class GKECreateAPIFilter(BaseModel):
    name: str
    location: str
    nodePools: List[GKENodePool]
    releaseChannel: GKEReleaseChannel
    resourceLabels: Dict


class GKECreateAPI(BaseModel):
    cluster: GKECreateAPIFilter


class GKEError(BaseModel):
    code: int
    message: str
    status: str


class GKEErrorResponse(BaseModel):
    error: GKEError
