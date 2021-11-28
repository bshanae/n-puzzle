from typing import Dict, Callable


from algo.n_puzzle import State
from reader.constants import PUZZLE_MAP_TYPE
from ui.console.info_storage import info


class TargetStateCalculator:
    _zero_last = -1
    _zero_first = -2
    _snail = -3

    def __init__(self, puzzle: PUZZLE_MAP_TYPE):
        self.puzzle = puzzle
        self.size = len(self.puzzle)
        self._target_funcs: Dict[int, Callable] = {
            self._snail: self.snail,
            self._zero_last: self.zero_last,
            self._zero_first: self.zero_first,
        }

    @property
    def state(self) -> State:
        """collect statistics to global var 'info'"""
        map_type = self._check_state_type(self.puzzle)
        calc_func: Callable = self._target_funcs[map_type]
        info.solution_type = calc_func.__name__

        return State(calc_func())

    def _check_state_type(self, puzzle: PUZZLE_MAP_TYPE):
        if puzzle[0][0] == 0:
            return self._zero_first
        elif puzzle[-1][-1] == 0:
            return self._zero_last
        else:
            return self._snail

    def snail(self) -> PUZZLE_MAP_TYPE:
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

    def zero_first(self) -> PUZZLE_MAP_TYPE:
        size = self.size
        sorted_puzzle = sorted(sum(self.puzzle, []))
        result = []
        for i in range(0, size * size, size):
            result.append(sorted_puzzle[i: i + size])

        return result

    def zero_last(self) -> PUZZLE_MAP_TYPE:
        size = self.size
        sorted_puzzle = sorted(sum(self.puzzle, []))
        zero = sorted_puzzle.pop(0)
        sorted_puzzle.insert(len(sorted_puzzle), zero)
        result = []
        for i in range(0, size * size, size):
            result.append(sorted_puzzle[i: i + size])

        return result


