from enum import Enum, unique
from typing import Dict, List, Optional

from pydantic import BaseModel


@unique
class ReleaseChannel(str, Enum):
    regular = "REGULAR"
    rapid = "RAPID"
    stable = "STABLE"


class GKEReleaseChannel(BaseModel):
    channel: ReleaseChannel = ReleaseChannel.stable


class GKEAutoscaling(BaseModel):
    enabled: bool = True
    min_node_count: int = 1
    max_node_count: int = 3


class GKEManagement(BaseModel):
    auto_upgrade: bool = True
    auto_repair: bool = True


class GKEUpgradeSettings(BaseModel):
    max_surge: int = 1


@unique
class AcceleratorType(str, Enum):
    nvidia_tesla_a100 = "nvidia-tesla-a100"
    nvidia_tesla_k80 = "nvidia-tesla-k80"
    nvidia_tesla_p100 = "nvidia-tesla-p100"
    nvidia_tesla_p4 = "nvidia-tesla-p4"
    nvidia_tesla_t4 = "nvidia-tesla-t4"
    nvidia_tesla_v100 = "nvidia-tesla-v100"


class Accelerator(BaseModel):
    accelerator_count: int = 1
    accelerator_type: AcceleratorType = AcceleratorType.nvidia_tesla_a100


class GKEShieldedInstanceConfig(BaseModel):
    enable_integrity_monitoring: bool = True


class GKENodePoolConfig(BaseModel):
    machine_type: str = "e2-medium"
    disk_size_gb: int = 20
    image_type: str = "COS"
    disk_type: str = "pd-ssd"
    accelerators: List[Accelerator] = []
    shielded_instance_config: GKEShieldedInstanceConfig = GKEShieldedInstanceConfig()
    metadata: Optional[Dict[str, str]] = {}
    labels: Optional[Dict[str, str]] = {}
    oauth_scopes: List[str] = [
        "https://www.googleapis.com/auth/devstorage.read_only",
        "https://www.googleapis.com/auth/logging.write",
        "https://www.googleapis.com/auth/monitoring",
        "https://www.googleapis.com/auth/servicecontrol",
        "https://www.googleapis.com/auth/service.management.readonly",
        "https://www.googleapis.com/auth/trace.append",
    ]


class GKENodePool(BaseModel):
    name: str
    initial_node_count: int
    config: GKENodePoolConfig = GKENodePoolConfig()
    autoscaling: GKEAutoscaling = GKEAutoscaling()
    management: GKEManagement = GKEManagement()
    upgrade_settings: GKEUpgradeSettings = GKEUpgradeSettings()


class GKEBase(BaseModel):
    name: str
    location: str
    node_pools: List[GKENodePool]
    release_channel: GKEReleaseChannel = GKEReleaseChannel()
    resource_labels: Optional[Dict[str, str]] = {}


class GKECluster(GKEBase):
    project_id: str


class GKEClusterApiFilter(GKEBase):
    pass


class GKEClusterOperationResponse(BaseModel):
    operation: str
    self_link: str
    target_link: str


class GCPProjectCreateOperationResponse(BaseModel):
    name: str
    done: str


@unique
class GCPServiceName(str, Enum):
    container = "container.googleapis.com"


class GCPSetupSpec(BaseModel):
    project_id: str
    service_name: GCPServiceName

    class Config:
        schema_extra = {
            "example": {
                "project_id": "my-project-123",
                "service_name": "container.googleapis.com",
            }
        }


class GKEClusterRead(BaseModel):
    name: str
    location: str
    project_id: str
