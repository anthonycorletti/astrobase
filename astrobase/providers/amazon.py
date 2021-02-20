from typing import List


class AmazonProvider:
    def __init__(self):
        pass

    def create_kubernetes_cluster(self) -> dict:
        pass

    def get_kubernetes_clusters(self) -> List[dict]:
        pass

    def describe_kubernetes_cluster(self) -> dict:
        pass

    def update_kubernetes_cluster(self) -> dict:
        pass

    def delete_kubernetes_cluster(self) -> dict:
        pass
