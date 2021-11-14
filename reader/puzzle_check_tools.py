from typing import Dict, Callable

import ipdb

from algo.n_puzzle import State
from reader.constants import PUZZLE_MAP_TYPE


class TargetStateCalculator:
    _zero_last = -1
    _zero_first = -2
    _snail = -3

    def __init__(self, puzzle: PUZZLE_MAP_TYPE):
        self.puzzle = puzzle
        self._target_funcs: Dict[int, Callable] = {
            self._snail: self.snail,
            self._zero_last: self.zero_last,
            self._zero_first: self.zero_first,
        }

    @property
    def state(self) -> State:
        map_type = self._check_state_type(self.puzzle)
        puzzle_len = len(self.puzzle)
        calc_func: Callable = self._target_funcs[map_type]
        return State(calc_func(puzzle_len))

    def _check_state_type(self, puzzle: PUZZLE_MAP_TYPE):
        if puzzle[0][0] == 0:
            return self._zero_first
        elif puzzle[-1][-1] == 0:
            return self._zero_last
        else:
            return self._snail

    @staticmethod
    def snail(size) -> PUZZLE_MAP_TYPE:
        # TODO: refactor it!
        lst = [[0 for _ in range(size)] for __ in range(size)]
        moves = [
            (0, 1),
            (1, 0),
            (0, -1),
            (-1, 0),
        ]
        row = col = 0
        i = 1
        final = size * size
        size -= 1
        while i is not final and size > 0:
            for move in moves:

                if i is final:
                    break

                for _ in range(size):
                    lst[row][col] = i
                    row += move[0]
                    col += move[1]
                    i += 1

                    if i is final:
                        break
            row += 1
            col += 1
            size -= 2

        return lst

    def zero_first(self, size) -> PUZZLE_MAP_TYPE:
        sorted_puzzle = sorted(sum(self.puzzle, []))
        result = []
        for i in range(0, size * size, size):
            result.append(sorted_puzzle[i: i + size])

        return result

    def zero_last(self, size) -> PUZZLE_MAP_TYPE:
        sorted_puzzle = sorted(sum(self.puzzle, []))
        zero = sorted_puzzle.pop(0)
        sorted_puzzle.insert(len(sorted_puzzle), zero)
        result = []
        for i in range(0, size * size, size):
            result.append(sorted_puzzle[i: i + size])

        return result


def check_solvable(start_state: State, target_state: State) -> bool:
    start_puzzle = start_state.listed_values
    target_puzzle = target_state.listed_values

    misplaced_tiles = 0
    for cur_pos in range(len(target_puzzle)):
        for next_pos in range(cur_pos + 1, len(target_puzzle)):
            cur_elem = start_puzzle[cur_pos]
            next_elem = start_puzzle[next_pos]
            if target_puzzle.index(cur_elem) > target_puzzle.index(next_elem):
                misplaced_tiles += 1

    current_row = start_state.zero_position // start_state.row_size
    current_col = start_state.zero_position % start_state.row_size
    target_row = target_state.zero_position // target_state.row_size
    target_col = target_state.zero_position % target_state.row_size

    zero_distance = abs(current_row - target_row) + abs(current_col - target_col)
    result = (not misplaced_tiles % 2) == (not zero_distance % 2)
    return result
