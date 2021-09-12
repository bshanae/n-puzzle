from typing import List

from algo import n_puzzle
from algo.solution_analyzer.move import Move
from algo.solution_analyzer.solution import Solution


def analyze_solution(path: List[n_puzzle.State]) -> Solution:
    moves: List[Move] = []

    for i in range(0, len(path) - 1):
        state_a = path[i]
        state_b = path[i + 1]

        moves.append(analyze_move(state_a, state_b))

    return Solution(path, moves)


def analyze_move(state_a: n_puzzle.State, state_b: n_puzzle.State) -> Move:
    index_a = next(state_a.diff_with(state_b))
    index_b = state_b.find(state_a[index_a])

    return Move(index_a, index_b)
