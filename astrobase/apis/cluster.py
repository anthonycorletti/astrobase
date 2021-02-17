from astrobase.providers.amazon import AmazonProvider
from astrobase.providers.google import GoogleProvider
from astrobase.schemas.cluster import Cluster, ClusterCreate

amazon_provider = AmazonProvider()
google_provider = GoogleProvider()


class ClusterAPI:
    def create_cluster(self, cluster_create: ClusterCreate) -> Cluster:
        return {
            "amazon": amazon_provider.create_cluster(cluster_create),
            "google": google_provider.create_cluster(cluster_create),
        }[cluster_create.platform]
