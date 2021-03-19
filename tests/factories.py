import yaml

EXAMPLES_DIR = "examples"


class ClusterFactory:
    CLUSTERS_DIR = "clusters"
    GKE_EXAMPLE = "gke.yaml"
    EKS_EXAMPLE = "eks.yaml"

    def gke_example(self) -> dict:
        example_file = f"{EXAMPLES_DIR}/{self.CLUSTERS_DIR}/{self.GKE_EXAMPLE}"
        with open(example_file, "r") as f:
            return yaml.safe_load(f).get("clusters")[0]

    def eks_example(self) -> dict:
        example_file = f"{EXAMPLES_DIR}/{self.CLUSTERS_DIR}/{self.EKS_EXAMPLE}"
        with open(example_file, "r") as f:
            return yaml.safe_load(f).get("clusters")[0]


class ResourceFactory:
    RESOURCES_DIR = "resources"
    KUBE_EXAMPLE = "resources.yaml"

    def kube_resources_example(self) -> dict:
        example_file = f"{EXAMPLES_DIR}/{self.RESOURCES_DIR}/{self.KUBE_EXAMPLE}"
        with open(example_file, "r") as f:
            return yaml.safe_load(f).get("resources")
