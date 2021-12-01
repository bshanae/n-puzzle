from typing import Callable, Tuple

from algo import n_puzzle
from algo.n_puzzle.heuristics import misplaced_tiles
from reader.constants import PUZZLE_MAP_TYPE, SNAIL, ZERO_LAST, ZERO_FIRST
from reader.puzzle_check_tools import TargetStateCalculator
from ui import info


def stat_collector_startup(func: Callable):
    """collect statistics to global var 'info'"""

    def wrapper(self, map_type: str):
        start_state, target_state, is_solvable = func(self, map_type)

        info.start_state = start_state.listed_values
        info.target_state = target_state.listed_values
        info.puzzle_size = start_state.size
        info.solution_type = self.solvable_target_type
        info.original_solution_type = self.original_target_type

        return start_state, target_state, is_solvable

    return wrapper


class StatesOnStart:
    def __init__(self, puzzle: PUZZLE_MAP_TYPE):
        self.puzzle = puzzle
        self.start_state = n_puzzle.State(puzzle)
        self.original_target_type: str = ''
        self.solvable_target_type: str = ''

    @stat_collector_startup
    def get_states_and_check_solvable(self, map_type: str) -> Tuple[n_puzzle.State, n_puzzle.State, bool]:
        self.original_target_type = map_type

        state_calculator = TargetStateCalculator(self.puzzle)
        target_state = state_calculator.state(map_type)
        if misplaced_tiles(self.start_state, target_state):
            self.solvable_target_type = map_type
            return self.start_state, target_state, True

        types_except_default = [t for t in [SNAIL, ZERO_LAST, ZERO_FIRST]]
        for new_type in types_except_default:
            for reverse in [True, False]:
                target_state = state_calculator.state(new_type, reverse=reverse)
                if misplaced_tiles(self.start_state, target_state):
                    self.solvable_target_type = new_type
                    return self.start_state, target_state, True

        return self.start_state, target_state, False
