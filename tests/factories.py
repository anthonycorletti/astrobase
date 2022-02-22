from typing import Dict

import yaml

TEST_ASSET_DIR = "examples"


class ClusterFactory:
    GKE_EXAMPLE = "simple-gke.yaml"
    EKS_EXAMPLE = "simple-eks.yaml"
    AKS_EXAMPLE = "simple-aks.yaml"

    def gke_example(self) -> Dict:
        example_file = f"{TEST_ASSET_DIR}/{self.GKE_EXAMPLE}"
        with open(example_file, "r") as f:
            return yaml.safe_load(f).get("clusters")[0]
