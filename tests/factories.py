import yaml

TEST_ASSET_DIR = "tests/assets"


class ClusterFactory:
    GKE_EXAMPLE = "test-gke-cluster.yaml"
    EKS_EXAMPLE = "test-eks-cluster.yaml"
    AKS_EXAMPLE = "test-aks-cluster.yaml"

    def gke_example(self) -> dict:
        example_file = f"{TEST_ASSET_DIR}/{self.GKE_EXAMPLE}"
        with open(example_file, "r") as f:
            return yaml.safe_load(f).get("clusters")[0]

    def eks_example(self) -> dict:
        example_file = f"{TEST_ASSET_DIR}/{self.EKS_EXAMPLE}"
        with open(example_file, "r") as f:
            return yaml.safe_load(f).get("clusters")[0]

    def aks_example(self) -> dict:
        example_file = f"{TEST_ASSET_DIR}/{self.AKS_EXAMPLE}"
        with open(example_file, "r") as f:
            return yaml.safe_load(f).get("clusters")[0]
