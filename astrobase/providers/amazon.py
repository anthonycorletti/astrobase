from astrobase.schemas.cluster import Cluster, ClusterCreate


class AmazonProvider:
    def create_cluster(self, cluster_create: ClusterCreate) -> Cluster:
        pass
