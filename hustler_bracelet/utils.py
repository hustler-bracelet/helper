import random


def create_int_uid() -> int:
    return int(''.join([str(random.randint(0, 9)) for _ in range(9)]))
