import os
from typing import Dict, List, Optional

from azure.mgmt.containerservice.models import (
    AgentPoolMode,
    ContainerServiceVMSizeTypes,
)
from pydantic import BaseModel


class ServicePrincipalProfile(BaseModel):
    client_id: Optional[str] = os.environ.get("AZURE_CLIENT_ID")
    secret: Optional[str] = os.environ.get("AZURE_CLIENT_SECRET")


class AgentPoolProfiles(BaseModel):
    name: str
    count: int = 2
    min_count: int = 2
    max_count: int = 3
    mode: AgentPoolMode
    tags: Dict[str, str] = {}
    os_disk_size_gb: int = 100
    enable_auto_scaling: bool = True
    node_labels: Dict[str, str] = {}
    vm_size: ContainerServiceVMSizeTypes = ContainerServiceVMSizeTypes(
        "Standard_DS2_v2"
    )


class AKSBase(BaseModel):
    name: str
    location: str
    dns_prefix: str
    resource_group_name: str
    enable_rbac: bool = True
    service_principal_profile: ServicePrincipalProfile = ServicePrincipalProfile()
    agent_pool_profiles: List[AgentPoolProfiles]
    tags: Dict[str, str] = {}


class AKSCluster(AKSBase):
    pass


class AKSClusterOperationResponse(BaseModel):
    message: str
