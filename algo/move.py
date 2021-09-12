from typing import Tuple


class Move:
    index_a: Tuple[int, int]
    index_b: Tuple[int, int]

    def __init__(self, index_a: Tuple[int, int], index_b: Tuple[int, int]):
        self.index_a = index_a
        self.index_b = index_b
