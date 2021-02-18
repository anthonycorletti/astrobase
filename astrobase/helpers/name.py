import random
import string


def random_name(k: int = 8) -> str:
    alphabet = string.ascii_lowercase + string.digits
    return "astrobase-" + "".join(random.choices(alphabet, k=8))
