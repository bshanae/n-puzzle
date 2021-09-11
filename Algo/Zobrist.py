import random

hash_codes = None


def init(dimension):
    global hash_codes

    hash_codes = []
    for i in range(0, dimension):
        hash_codes.append([])
        for j in range(0, dimension):
            hash_codes[i].append([])
            for k in range(0, dimension * dimension):
                hash_codes[i][j].append(random.randint(1, 2 ** 64 - 1))


def hash(table):
    if hash_codes is None:
        init(len(table))

    hash_result = 0

    for i in range(len(table)):
        for j in range(len(table[i])):
            value = table[i][j]
            hash_result ^= hash_codes[i][j][value]

    return hash_result
