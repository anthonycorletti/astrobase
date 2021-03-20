from typing import List

from pydantic import BaseModel


class Clusters(BaseModel):
    """
    Cluster schema validation happens on the astrobase api because
    the api has to orchestrate a asynchronous api calls to cloud providers.

    Here, we only confirm that we atleast have a leading `clusters` key.
    """

    clusters: List[dict] = []
