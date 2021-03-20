import random
import string

VOWELS = "aeiou"
CHARACTERS = string.ascii_lowercase + string.digits
CONSONANTS = "".join(set(string.ascii_lowercase) - set(VOWELS))


def random_name(k: int = 7) -> str:
    word = ""
    suffix = "".join(random.choices(CHARACTERS, k=k))
    for i in range(k):
        if i % 2 == 0:
            word += random.choice(CONSONANTS)
        else:
            word += random.choice(VOWELS)
    return f"{word}-{suffix}"
