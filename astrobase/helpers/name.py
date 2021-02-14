import random
import string


class NameHelper:
    def random_name(self, k: int = 8) -> str:
        alphabet = string.ascii_lowercase + string.digits
        return "".join(random.choices(alphabet, k=8))
