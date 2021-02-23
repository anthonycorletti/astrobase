from pydantic import BaseModel


class KubernetesServiceBase(BaseModel):
    kubernetes_cluster_name: str
    kubernetes_resource_dir: str


class KubernetesServiceCreate(KubernetesServiceBase):
    pass


class KubernetesServiceUpdate(KubernetesServiceBase):
    pass


class KubernetesService(KubernetesServiceBase):
    pass
