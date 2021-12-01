from typing import Optional

from algo import n_puzzle, solution_analyzer
from ui.console.info_storage import info


def present_statistics(is_solvable: bool):
    if info.original_solution_type != info.solution_type:
        print(f'Note!\tPuzzle is unsolvable in given target state: {info.original_solution_type}')
        print(f'\tFind solvable target state: {info.solution_type}\n')

    print('algo:', info.algo)
    print('heuristic:', info.h_function)
    print('greedy search:', info.greedy)
    print('uniform-cost search:', info.uniform)
    print('puzzle size:', info.puzzle_size)

    if info.original_solution_type == info.solution_type:
        print('solution type:', info.solution_type)
    print('start state:', info.start_state)
    print('target state:', info.target_state)

    if not is_solvable:
        print('This puzzle is unsolvable in any target states!')
        return

    print('moves to solve:', info.moves_ct)
    print('time complexity:', info.time_complexity)
    print('size complexity:', info.size_complexity)
    print('search duration:', f'{info.duration:.6f} sec')
    print('process resources in RAM (max rss):', info.max_rss, '\n')


def present_solution(solution: solution_analyzer.Solution):
    for i in range(len(solution.states)):
        if i >= 1:
            print_state(solution.states[i], solution.moves[i - 1])
        else:
            print_state(solution.states[i], None)


def print_state(state: n_puzzle.State, move: Optional[solution_analyzer.Move]):
    HIGHLIGHT = '\u001b[36m'
    RESET = '\033[0m'

    line = ''

    for i in range(len(state.values)):
        for j in range(len(state.values[i])):
            value = state[i, j]

            if value is not None:
                if move is not None and ((i, j) == move.index_a or (i, j) == move.index_b):
                    line += '{}{:2}{} '.format(HIGHLIGHT, value, RESET)
                else:
                    line += '{:2} '.format(value)
            else:
                line += '   '

        line += '\n\r'

    print(line)
