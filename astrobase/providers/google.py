from googleapiclient.discovery import build

from astrobase.schemas.cluster import GoogleCluster, GoogleClusterCreate


class GoogleProvider:
    def __init__(self):
        self.client = build("container", "v1beta1")
        self.cluster_client = self.client.projects().zones().clusters()

    def create_cluster(self, cluster_create: GoogleClusterCreate) -> GoogleCluster:
        example_data = {
            "cluster": {
                "name": "cluster-1",
                "masterAuth": {"clientCertificateConfig": {}},
                "network": "projects/astrobase-284118/global/networks/default",
                "addonsConfig": {
                    "httpLoadBalancing": {},
                    "horizontalPodAutoscaling": {},
                    "kubernetesDashboard": {"disabled": "true"},
                    "dnsCacheConfig": {},
                    "gcePersistentDiskCsiDriverConfig": {},
                },
                "subnetwork": "projects/astrobase-284118/regions/us-central1/subnetworks/default",
                "nodePools": [
                    {
                        "name": "default-pool",
                        "config": {
                            "machineType": "e2-medium",
                            "diskSizeGb": 100,
                            "oauthScopes": [
                                "https://www.googleapis.com/auth/devstorage.read_only",
                                "https://www.googleapis.com/auth/logging.write",
                                "https://www.googleapis.com/auth/monitoring",
                                "https://www.googleapis.com/auth/servicecontrol",
                                "https://www.googleapis.com/auth/service.management.readonly",
                                "https://www.googleapis.com/auth/trace.append",
                            ],
                            "metadata": {"disable-legacy-endpoints": "true"},
                            "imageType": "COS",
                            "diskType": "pd-standard",
                            "shieldedInstanceConfig": {
                                "enableIntegrityMonitoring": "true"
                            },
                        },
                        "initialNodeCount": 3,
                        "autoscaling": {},
                        "management": {"autoUpgrade": "true", "autoRepair": "true"},
                        "upgradeSettings": {"maxSurge": 1},
                    }
                ],
                "locations": ["us-central1-a"],
                "networkPolicy": {},
                "ipAllocationPolicy": {"useIpAliases": "true"},
                "masterAuthorizedNetworksConfig": {},
                "autoscaling": {},
                "defaultMaxPodsConstraint": {"maxPodsPerNode": "110"},
                "authenticatorGroupsConfig": {},
                "privateClusterConfig": {},
                "databaseEncryption": {"state": "DECRYPTED"},
                "shieldedNodes": {},
                "releaseChannel": {"channel": "REGULAR"},
                "clusterTelemetry": {"type": "ENABLED"},
                "notificationConfig": {"pubsub": {}},
                "initialClusterVersion": "1.17.15-gke.800",
                "location": "us-central1-a",
            }
        }
        print()
        print(cluster_create.json())
        print()
        req = self.cluster_client.create(
            body=example_data,
            projectId=cluster_create.project_id,
            zone=cluster_create.zone,
        )
        res = req.execute()
        print(res)
