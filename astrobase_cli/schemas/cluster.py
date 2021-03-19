from typing import List

from pydantic import BaseModel


class Clusters(BaseModel):
    """
    The majority of cluster schema validation happens on
    the astrobase api as it orchestrates a few asynchronous
    api calls to cloud providers. Here, we only confirm that
    we have a leading `clusters` key.
    """

    clusters: List[dict] = []
