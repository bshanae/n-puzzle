import random
from typing import List

is_initialized = False
hash_codes: List[List[List[int]]]


def initialize_if_needed(dimension: int):
    global is_initialized
    if is_initialized:
        return

    global hash_codes
    hash_codes = []

    for i in range(0, dimension):
        hash_codes.append([])
        for j in range(0, dimension):
            hash_codes[i].append([])
            for k in range(0, dimension * dimension):
                hash_codes[i][j].append(random.randint(1, 2 ** 64 - 1))

    is_initialized = True


def hash(table: List[List[int]]) -> int:
    initialize_if_needed(len(table))

    hash_result = 0

    for i in range(len(table)):
        for j in range(len(table[i])):
            value = table[i][j]
            hash_result ^= hash_codes[i][j][value]

    return hash_result
