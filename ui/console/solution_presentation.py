from typing import Optional

from algo import n_puzzle, solution_analyzer


def present_solution(solution: solution_analyzer.Solution):
    for i in range(len(solution.states)):
        if i >= 1:
            print_state(solution.states[i], solution.moves[i - 1])
        else:
            print_state(solution.states[i], None)


def print_state(state: n_puzzle.State, move: Optional[solution_analyzer.Move]):
    HIGHLIGHT = '\u001b[36m'
    RESET = '\033[0m'

    str = ""

    for i in range(len(state.values)):
        for j in range(len(state.values[i])):
            value = state[i, j]

            if value is not None:
                if move is not None and ((i, j) == move.index_a or (i, j) == move.index_b):
                    str += "{}{:2}{} ".format(HIGHLIGHT, value, RESET)
                else:
                    str += "{:2} ".format(value)
            else:
                str += "   "

        str += "\n\r"

    print(str)
