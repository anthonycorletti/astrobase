import random
import string

VOWELS = "aeiou"
CONSONANTS = "".join(set(string.ascii_lowercase) - set(VOWELS))


def random_word(k: int = 7) -> str:
    word = ""
    for i in range(k):
        if i % 2 == 0:
            word += random.choice(CONSONANTS)
        else:
            word += random.choice(VOWELS)
    return word


def random_name(k: int = 7) -> str:
    characters = string.ascii_lowercase + string.digits
    suffix = "".join(random.choices(characters, k=k))
    return f"{random_word(k)}-{suffix}"
