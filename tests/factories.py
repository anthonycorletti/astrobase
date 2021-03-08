class ClusterFactory:
    gke_create_example = {
        "name": "astrobase-test-gke",
        "project_id": "astrobase-284118",
        "location": "us-central1",
    }

    eks_create_example = {
        "name": "astrobase-test-eks-2",
        "roleArn": "arn:aws:iam::541181908229:role/AstrobaseEKSRole",
        "resourcesVpcConfig": {
            "subnetIds": ["subnet-a023bbff", "subnet-987d53d5"],
            "securityGroupIds": ["sg-67306a6a"],
            "endpointPublicAccess": True,
            "endpointPrivateAccess": True,
        },
        "logging": {
            "clusterLogging": [
                {
                    "types": [
                        "api",
                        "audit",
                        "authenticator",
                        "controllerManager",
                        "scheduler",
                    ],
                    "enabled": True,
                }
            ]
        },
    }


class ResourceFactory:
    gke_resource_example = {
        "name": "simple-nginx",
        "provider": "gke",
        "resource_dir": "kubernetes",
        "cluster_name": "astrobase-test-gke",
    }
