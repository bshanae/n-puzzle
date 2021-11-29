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
    puzzles = parser.puzzles
    greedy, uniform = parser.greedy_and_uniform

    algo = a_star.Algo(h_function=parser.h_function, greedy=greedy, uniform=uniform,)

    for index, puzzle in enumerate(puzzles):
        print('Begin solvation...\n')
        start_state, target_state = get_states_on_start(puzzle)
        is_solvable = misplaced_tiles(start_state, target_state)

        if not is_solvable:
            ui.present_solution(None, parser.use_console, parser.use_gui, index == len(puzzles) - 1)
            continue

        solution_states = algo.solve(start_state, target_state)

        solution = solution_analyzer.analyze_solution(solution_states)
        ui.present_solution(solution, parser.use_console, parser.use_gui, index == len(puzzles) - 1)

    sys.exit(0)


if __name__ == '__main__':
    do_solvation()
