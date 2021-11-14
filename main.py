import sys
from typing import List

from algo import n_puzzle, a_star, solution_analyzer
import ui
from reader.argument_parser import ArgParser
from time import time

from reader.constants import PUZZLE_MAP_TYPE
from reader.puzzle_check_tools import TargetStateCalculator, check_solvable


def parse_puzzles(map_file: str) -> List[PUZZLE_MAP_TYPE]:
    puzzles = []
    with open(map_file, 'r') as f:
        for _ in range(2):
            next(f)
        puzzle = []
        lines = f.readlines()
        for line in lines:
            if line != '\n':
                puzzle.append(list(map(int, line.split())))
            else:
                puzzles.append(puzzle)
                puzzle = []

    if puzzle and not puzzles:
        puzzles.append(puzzle)
    return puzzles


def do_solvation():
    parser = ArgParser()
    args = parser.args
    src_file = args.map_file

    maps = parse_puzzles(src_file)

    algo = a_star.Algo(n_puzzle.heuristics.manhattan)
    algo.is_greedy = False
    algo.is_uniform = False

    for one in maps:
        st_state = n_puzzle.State(one)
        tg_state = TargetStateCalculator(one).state
        print('Start state:', st_state.values)
        print('Target state:', tg_state.values)

        is_solvable = check_solvable(st_state, tg_state)
        if not is_solvable:
            print("UNSOLVABLE!!!")
            sys.exit(0)

        start = time()
        solution_states = algo.solve(st_state, tg_state)
        dur = time() - start

        print(f'{dur:0.6f}')

        solution = solution_analyzer.analyze_solution(solution_states)
        ui.present_solution(solution)
    sys.exit(0)


if __name__ == '__main__':
    do_solvation()
