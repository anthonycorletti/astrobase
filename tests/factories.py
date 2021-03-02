class ClusterFactory:
    gke_create_example = {
        "name": "astrobase-test-gke",
        "project_id": "astrobase-284118",
        "location": "us-central1",
    }


class ResourceFactory:
    gke_resource_example = {
        "name": "simple-nginx",
        "provider": "gke",
        "resource_dir": "kubernetes",
        "cluster_name": "astrobase-test-gke",
    }
