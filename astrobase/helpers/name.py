import random
import string


def random_name(component: str, k: int = 8) -> str:
    alphabet = string.ascii_lowercase + string.digits
    return "astrobase-" + f"-{component}-" + "".join(random.choices(alphabet, k=8))
