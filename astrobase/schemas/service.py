from typing import Optional

from pydantic import BaseModel, Field

from astrobase.helpers.name import random_name


class KubernetesServiceBase(BaseModel):
    kubernetes_cluster_name: str
    helm_chart_root: str = "astrobase"


class KubernetesServiceCreate(KubernetesServiceBase):
    pass


class KubernetesServiceUpdate(KubernetesServiceBase):
    pass


class KubernetesService(KubernetesServiceBase):
    pass
