from enum import Enum, unique
from typing import Dict, List, Optional, Union

from pydantic import BaseModel, Field, validator

from astrobase.helpers.name import random_name


class ResourcesVpcConfig(BaseModel):
    subnetIds: List[str]
    securityGroupIds: List[str]
    endpointPublicAccess: bool
    endpointPrivateAccess: bool
    publicAccessCidrs: List[str] = ["0.0.0.0/0"]


@unique
class ClusterLoggingType(str, Enum):
    api = "api"
    audit = "audit"
    authenticator = "authenticator"
    controllerManager = "controllerManager"
    scheduler = "scheduler"


class ClusterLogging(BaseModel):
    clusterLogging: List[Dict[str, Union[List[ClusterLoggingType], bool]]]


class EKSBase(BaseModel):
    name: Optional[str] = Field(default_factory=random_name)
    region: str
    roleArn: str
    resourcesVpcConfig: ResourcesVpcConfig
    tags: Optional[Dict[str, str]] = {}
    logging: Optional[ClusterLogging] = {}

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
    logging: Optional[ClusterLogging] = {}


class EKS(EKSBase):
    pass


class EKSCreateFilter(BaseModel):
    name: str


class EKSCreateAPI(BaseModel):
    cluster: EKSCreateFilter
