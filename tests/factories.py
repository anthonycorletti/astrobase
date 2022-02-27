from typing import Dict

import yaml

from astrobase.types.gcp import GCPSetupSpec

TEST_ASSET_DIR = "examples"


class ClusterFactory:
    GKE_EXAMPLE = "simple-gke.yaml"
    EKS_EXAMPLE = "simple-eks.yaml"
    AKS_EXAMPLE = "simple-aks.yaml"

    def gke_example(self) -> Dict:
        example_file = f"{TEST_ASSET_DIR}/{self.GKE_EXAMPLE}"
        with open(example_file, "r") as f:
            return yaml.safe_load(f).get("cluster")

    def eks_example(self) -> Dict:
        example_file = f"{TEST_ASSET_DIR}/{self.EKS_EXAMPLE}"
        with open(example_file, "r") as f:
            return yaml.safe_load(f).get("cluster")

    def aks_example(self) -> Dict:
        example_file = f"{TEST_ASSET_DIR}/{self.EKS_EXAMPLE}"
        with open(example_file, "r") as f:
            return yaml.safe_load(f).get("cluster")


class GCPSetupSpecFactory:
    def setup_container_api_spec(self) -> GCPSetupSpec:
        return GCPSetupSpec(
            project_id="test-1234", service_name="container.googleapis.com"
        )
