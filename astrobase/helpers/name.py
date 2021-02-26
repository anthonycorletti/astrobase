import random
import string


def random_cluster_name(k: int = 8) -> str:
    alphabet = string.ascii_lowercase + string.digits
    return "astrobase-cluster-" + "".join(random.choices(alphabet, k=k))
