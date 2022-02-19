from enum import Enum, unique


@unique
class Provider(str, Enum):
    gcp = "gcp"
    eks = "eks"
    aks = "aks"
