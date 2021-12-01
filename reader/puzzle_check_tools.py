from typing import Dict, Callable

from algo.n_puzzle import State
from reader.constants import PUZZLE_MAP_TYPE, SNAIL, ZERO_LAST, ZERO_FIRST


class TargetStateCalculator:

    def __init__(self, puzzle: PUZZLE_MAP_TYPE):
        self.puzzle = puzzle
        self.size = len(self.puzzle)
        self._target_funcs: Dict[str, Callable] = {
            SNAIL: self.snail,
            ZERO_LAST: self.zero_last,
            ZERO_FIRST: self.zero_first,
        }

    def state(self, map_type: str, reverse: bool = False) -> State:
        calc_func: Callable = self._target_funcs[map_type]
        return State(calc_func(reverse))

    def snail(self, reverse: bool) -> PUZZLE_MAP_TYPE:
        size = self.size
        puzzle = [[0] * size for _ in range(size)]
        row_offsets = [0, 1, 0, -1]
        col_offsets = [1, 0, -1, 0]
        row = 0
        col = -1
        val = 1
        for i in range(size + size - 1):
            for _ in range((size + size - i) // 2):
                row += row_offsets[i % 4]
                col += col_offsets[i % 4]
                puzzle[row][col] = val
                val = 0 if val == size * size - 1 else val + 1  # fill zero position

        return puzzle

    def zero_first(self, reverse: bool) -> PUZZLE_MAP_TYPE:
        size = self.size
        sorted_puzzle = sorted(sum(self.puzzle, []), reverse=reverse)
        result = []
        for i in range(0, size * size, size):
            result.append(sorted_puzzle[i: i + size])

        return result

    def zero_last(self, reverse: bool) -> PUZZLE_MAP_TYPE:
        size = self.size
        sorted_puzzle = sorted(sum(self.puzzle, []), reverse=reverse)
        zero = sorted_puzzle.pop(0)
        sorted_puzzle.insert(len(sorted_puzzle), zero)
        result = []
        for i in range(0, size * size, size):
            result.append(sorted_puzzle[i: i + size])

        return result


