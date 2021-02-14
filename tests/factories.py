import uuid


class ClusterFactory:
    google_example = {
        "id": uuid.uuid4(),
        "name": "astrobase-test-cluster",
        "platform": "google",
    }
