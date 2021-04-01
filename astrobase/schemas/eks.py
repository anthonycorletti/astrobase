from enum import Enum, unique
from typing import Dict, List, Optional

from pydantic import BaseModel, Field, validator

from astrobase.helpers.name import random_name


class EKSNodegroupScalingConfig(BaseModel):
    minSize: int = 1
    maxSize: int = 3
    desiredSize: int = 1


@unique
class EKSNodegroupAmiType(str, Enum):
    al2_x86_64 = "AL2_x86_64"
    al2_x86_64_gpu = "AL2_x86_64_GPU"
    al2_arm_64 = "AL2_ARM_64"


@unique
class EKSNodegroupCapacityType(str, Enum):
    on_demand = "ON_DEMAND"
    spot = "SPOT"


class EKSNodegroup(BaseModel):
    clusterName: str
    nodegroupName: str
    scalingConfig: EKSNodegroupScalingConfig
    diskSize: int = 100
    subnets: List[str]
    instanceTypes: List[str] = ["t3.medium"]
    amiType: EKSNodegroupAmiType = EKSNodegroupAmiType.al2_x86_64
    nodeRole: str
    labels: Optional[Dict[str, str]] = {}
    tags: Optional[Dict[str, str]] = {}
    capacityType: EKSNodegroupCapacityType = EKSNodegroupCapacityType.spot


class ResourcesVpcConfig(BaseModel):
    subnetIds: List[str]
    securityGroupIds: List[str]
    endpointPublicAccess: bool = True
    endpointPrivateAccess: bool = True
    publicAccessCidrs: List[str] = ["0.0.0.0/0"]


@unique
class ClusterLoggingType(str, Enum):
    api = "api"
    audit = "audit"
    scheduler = "scheduler"
    authenticator = "authenticator"
    controllerManager = "controllerManager"


class ClusterLoggingConfig(BaseModel):
    types: List[ClusterLoggingType] = []
    enabled: bool = False


class ClusterLogging(BaseModel):
    clusterLogging: List[ClusterLoggingConfig] = [ClusterLoggingConfig()]


class EKSBase(BaseModel):
    name: Optional[str] = Field(default_factory=random_name)
    region: str
    roleArn: str
    resourcesVpcConfig: ResourcesVpcConfig
    tags: Optional[Dict[str, str]] = {}
    logging: ClusterLogging = ClusterLogging()
    nodegroups: List[EKSNodegroup]

    @validator("name")
    def name_is_set(cls, name: str) -> str:
        if not name:
            return random_name()
        return name


class EKSCreate(EKSBase):
    pass


class EKSCreateAPIFilter(BaseModel):
    name: str
    roleArn: str
    resourcesVpcConfig: ResourcesVpcConfig
    tags: Optional[Dict[str, str]] = {}
    logging: Optional[ClusterLogging] = ClusterLogging()
