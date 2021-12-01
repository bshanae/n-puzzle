import sys

from algo import a_star, solution_analyzer
import ui
from reader.argument_parser import ArgParser
from reader.on_startup import StatesOnStart


def do_solvation():
    parser = ArgParser()
    puzzles = parser.puzzles
    greedy, uniform = parser.greedy_and_uniform
    map_type = parser.map_type

    algo = a_star.Algo(h_function=parser.h_function, greedy=greedy, uniform=uniform,)

    for index, puzzle in enumerate(puzzles):
        print('Begin solvation...\n')
        on_start = StatesOnStart(puzzle)
        start_state, target_state, is_solvable = on_start.get_states_and_check_solvable(map_type)

        if not is_solvable:
            ui.present_solution(None, parser.use_console, parser.use_gui, index == len(puzzles) - 1)
            continue

        solution_states = algo.solve(start_state, target_state)

        solution = solution_analyzer.analyze_solution(solution_states)
        ui.present_solution(solution, parser.use_console, parser.use_gui, index == len(puzzles) - 1)

    sys.exit(0)


if __name__ == '__main__':
    do_solvation()
