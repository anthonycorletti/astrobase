import random
import string

VOWELS = "aeiou"
CONSONANTS = "".join(set(string.ascii_lowercase) - set(VOWELS))


def prefix_name(k: int = 7):
    word = ""
    for i in range(k):
        if i % 2 == 0:
            word += random.choice(CONSONANTS)
        else:
            word += random.choice(VOWELS)
    return word


def random_name(k: int = 7) -> str:
    alphabet = string.ascii_lowercase + string.digits
    prefix = prefix_name(k)
    suffix = "".join(random.choices(alphabet, k=k))
    return f"{prefix}-{suffix}"
