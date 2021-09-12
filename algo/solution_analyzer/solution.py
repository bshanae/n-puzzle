from typing import List

from algo import n_puzzle
from algo.solution_analyzer.move import Move


class Solution:
    states: List[n_puzzle.State]
    moves: List[Move]

    def __init__(self, states: List[n_puzzle.State], moves: List[Move]):
        self.states = states
        self.moves = moves
