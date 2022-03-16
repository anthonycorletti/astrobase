from typing import Dict

import yaml

from astrobasecloud.types.gcp import GCPSetupSpec

TEST_ASSET_DIR = "examples"


class ClusterFactory:
    GKE_EXAMPLE = "simple-gke.yaml"
    EKS_EXAMPLE = "simple-eks.yaml"
    AKS_EXAMPLE = "simple-aks.yaml"

    def gke_example(self) -> Dict:
        example_file = f"{TEST_ASSET_DIR}/{self.GKE_EXAMPLE}"
        with open(example_file, "r") as f:
            return yaml.safe_load(f).get("cluster")

    def gke_example_complete_spec(self) -> Dict:
        cluster_spec = self.gke_example()
        cluster_spec["project_id"] = "testProject"
        return cluster_spec

    def eks_example(self) -> Dict:
        example_file = f"{TEST_ASSET_DIR}/{self.EKS_EXAMPLE}"
        with open(example_file, "r") as f:
            return yaml.safe_load(f).get("cluster")

    def eks_example_complete_spec(self) -> Dict:
        cluster_spec = self.eks_example()
        cluster_spec[
            "roleArn"
        ] = "arn:aws:iam::000000000001:role/AstrobaseEKSClusterRole"
        cluster_spec["resourcesVpcConfig"] = {}
        cluster_spec["resourcesVpcConfig"]["subnetIds"] = [
            "subnet-000001",
            "subnet-000002",
        ]
        cluster_spec["resourcesVpcConfig"]["securityGroupIds"] = [
            "sg-000001",
            "sg-000002",
        ]
        for ng in cluster_spec["nodegroups"]:
            ng["nodeRole"] = "arn:aws:iam::000000000001:role/AstrobaseEKSNodegroupRole"
        return cluster_spec

    def aks_example(self) -> Dict:
        example_file = f"{TEST_ASSET_DIR}/{self.AKS_EXAMPLE}"
        with open(example_file, "r") as f:
            return yaml.safe_load(f).get("cluster")

    def aks_example_complete_spec(self) -> Dict:
        cluster_spec = self.aks_example()
        cluster_spec["resource_group_name"] = "test-rg"
        return cluster_spec


class GCPSetupSpecFactory:
    def setup_container_api_spec(self) -> GCPSetupSpec:
        return GCPSetupSpec(
            project_id="test-1234", service_name="container.googleapis.com"
        )
