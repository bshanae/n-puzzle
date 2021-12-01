import copy
from typing import List, Tuple

from algo.n_puzzle import zobrist
import uuid


class State:
    def __init__(self, values: List[List[int]]):
        self.values: List[List[int]] = values
        self.hash: int = zobrist.hash(self.values)
        self.id = uuid.uuid4()

    def __eq__(self, other) -> bool:
        return self.hash == other.hash

    def __getitem__(self, idx: Tuple[int, int]) -> int:
        row_index, value_index = idx
        return self.values[row_index][value_index]

    def __setitem__(self, index: Tuple[int, int], value: int):
        row_index, value_index = index
        self.values[row_index][value_index] = value

    def __hash__(self) -> int:
        return self.hash

    def __str__(self):
        str_repr = ""

        for row in self.values:
            for value in row:
                if value is not None:
                    str_repr += ("{:2} ".format(value))
                else:
                    str_repr += "   "

            str_repr += "\n\r"

        return str_repr

    @property
    def listed_values(self) -> list:
        return sum(self.values, [])

    @property
    def size(self) -> int:
        return len(self.values[0])

    def columns(self) -> list:
        return [list(col) for col in (zip(*self.values))]

    def zero_position(self) -> Tuple[int, int]:
        zero_index = self.listed_values.index(0)
        return zero_index // self.size, zero_index % self.size

    def expand(self) -> 'State':
        def apply_offset_on_index(idx: Tuple[int, int]):
            offsets = [(+1, 0),
                       (-1, 0),
                       (0, +1),
                       (0, -1)]

            row_index, value_index = idx

            for offset_row, offset_value in offsets:
                test_index = row_index + offset_row, value_index + offset_value
                if self.is_valid_index(test_index):
                    yield test_index

        def clone_and_swap(index_a: Tuple[int, int], index_b: Tuple[int, int]) -> 'State':
            row_index_a, value_index_a = index_a
            row_index_b, value_index_b = index_b

            new_values = copy.deepcopy(self.values)

            temporary = new_values[row_index_a][value_index_a]
            new_values[row_index_a][value_index_a] = new_values[row_index_b][value_index_b]
            new_values[row_index_b][value_index_b] = temporary

            return State(new_values)

        combinations = set()
        for index, value in self.enumerate():
            for offset_index in apply_offset_on_index(index):
                new_combination = clone_and_swap(index, offset_index)
                h = hash(new_combination)
                if h not in combinations:
                    combinations.add(h)
                    yield new_combination

    cached_enumeration: List[Tuple[Tuple[int, int], int]] = None

    def enumerate(self) -> List[Tuple[Tuple[int, int], int]]:
        if self.cached_enumeration is None:
            self.cached_enumeration = []

            for i in range(len(self.values)):
                for j in range(len(self.values[i])):
                    self.cached_enumeration.append(((i, j), self.values[i][j]))

        return self.cached_enumeration

    def find(self, target_value: int) -> Tuple[int, int]:
        for (row_index, value_index), value in self.enumerate():
            if value == target_value:
                return row_index, value_index

        raise Exception(f"Value {target_value} not found")

    def is_valid_index(self, index: Tuple[int, int]) -> bool:
        row_index, value_index = index

        if row_index < 0 or row_index >= len(self.values):
            return False

        if value_index < 0 or value_index >= len(self.values[0]):
            return False

        return True

    def diff_with(self, other) -> List[Tuple[int, int]]:
        for i in range(len(self.values)):
            for j in range(len(self.values[i])):
                if self[i, j] != other[i, j]:
                    yield i, j
