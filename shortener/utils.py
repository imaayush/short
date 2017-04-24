from random import SystemRandom

from string import ascii_letters, digits

DEFAULT_SHORT_LEN = 16


def generate_random_id(length=DEFAULT_SHORT_LEN, choice=ascii_letters + digits):
    """
    generate a temporary random id
    be careful because of small length it may not be unique
    """
    rnd = SystemRandom()
    uid = ""
    for idx in range(0, length):
        uid += rnd.choice(choice)
    return uid
