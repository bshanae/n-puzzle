import sys
from typing import Tuple

from algo import n_puzzle, a_star, solution_analyzer
import ui
from reader.argument_parser import ArgParser

from reader.constants import PUZZLE_MAP_TYPE
from reader.puzzle_check_tools import TargetStateCalculator
from algo.n_puzzle.heuristics import misplaced_tiles
from ui.console.info_storage import info


def get_states_on_start(puzzle: PUZZLE_MAP_TYPE) -> Tuple[n_puzzle.State, n_puzzle.State]:
    """collect statistics to global var 'info'"""
    start_state = n_puzzle.State(puzzle)
    target_state = TargetStateCalculator(puzzle).state

    info.start_state = start_state.listed_values
    info.target_state = target_state.listed_values
    info.puzzle_size = start_state.size

    return start_state, target_state


def do_solvation():
    parser = ArgParser()
    maps = parser.puzzles
    greedy, uniform = parser.greedy_and_uniform
    gui_enabled, console_enabled = parser.gui_and_console
    heuristic = parser.h_function

    algo = a_star.Algo(
        h_function=heuristic,
        greedy=greedy,
        uniform=uniform,
    )

    for one in maps:
        print('Begin solvation...\n')
        start_state, target_state = get_states_on_start(one)
        is_solvable = misplaced_tiles(start_state, target_state)

        if not is_solvable:
            ui.present_solution(None, gui_enabled, console_enabled)
            continue

        solution_states = algo.solve(start_state, target_state)

        solution = solution_analyzer.analyze_solution(solution_states)
        ui.present_solution(solution, gui_enabled, console_enabled)
    sys.exit(0)


if __name__ == '__main__':
    do_solvation()
