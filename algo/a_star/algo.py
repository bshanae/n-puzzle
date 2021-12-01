import sys
from queue import PriorityQueue
from collections import deque
from typing import Deque, Optional, Callable

import resource

from algo.a_star.state_wrap import StateWrap
from algo.n_puzzle import State
from ui.console.info_storage import info
from time import time


def algo_stat_collector(func: Callable):
    """collect statistics to global var 'info'"""

    def wrapper(self, start_state: State, target_state: State):
        start = time()
        solution = func(self, start_state, target_state)
        duration = time() - start

        info.greedy = self.is_greedy
        info.uniform = self.is_uniform
        info.h_function = self.h_function.__name__
        info.algo = self._algo
        info.size_complexity = self._size_complexity
        info.time_complexity = self._time_complexity
        info.duration = duration
        info.moves_ct = len(solution)
        info.max_rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

        return solution

    return wrapper


class Algo:
    _algo = 'A*'

    def __init__(self, h_function: Callable, greedy: bool, uniform: bool):
        self.h_function = h_function
        self.is_greedy = greedy
        self.is_uniform = uniform
        self._size_complexity = 0
        self._time_complexity = 0

    @algo_stat_collector
    def solve(self, start_state: State, target_state: State) -> Optional[Deque]:
        closed_state_wraps = {}
        opened_states = {}

        start_state_wrap = StateWrap(
            h_value=self.compute_h(start_state, target_state),
            g_value=self.compute_g(None),
            state=start_state,
        )

        open_state_wraps = PriorityQueue()
        open_state_wraps.put((start_state_wrap.f_value, start_state_wrap))

        while open_state_wraps:
            f_value, current_state_wrap = open_state_wraps.get()

            if current_state_wrap.state == target_state:
                self._size_complexity = len(closed_state_wraps)
                self._time_complexity = open_state_wraps.qsize()
                return self.restore_path(current_state_wrap)

            closed_state_wraps[current_state_wrap.__hash__()] = current_state_wrap

            for expanded_state in current_state_wrap.state.expand():
                expanded_state_wrap = StateWrap(
                    h_value=self.compute_h(expanded_state, target_state),
                    g_value=self.compute_g(current_state_wrap),
                    state=expanded_state,
                    previous_state=current_state_wrap,
                )
                if closed_state_wraps.get(expanded_state_wrap.__hash__(), None):
                    continue

                opened_state_wrap = opened_states.get(expanded_state_wrap.__hash__(), None)
                if opened_state_wrap and opened_state_wrap.f_value >= expanded_state_wrap.f_value:
                    opened_states[expanded_state_wrap.__hash__()] = expanded_state_wrap
                    continue

                opened_states[expanded_state_wrap.__hash__()] = expanded_state_wrap
                open_state_wraps.put((expanded_state_wrap.f_value, expanded_state_wrap))

        self._size_complexity = len(closed_state_wraps)
        self._time_complexity = open_state_wraps.qsize()
        return None

    def compute_h(self, current_state: State, target_state: State) -> int:
        if self.is_uniform:
            return 0
        return self.h_function(current_state, target_state)

    def compute_g(self, previous_state: Optional[StateWrap]) -> int:
        if self.is_greedy:
            return 0

        if previous_state is not None:
            return previous_state.g_value + 1
        else:
            return 0

    @staticmethod
    def restore_path(final_state) -> Deque:
        path = deque()

        iterator_state = final_state
        while iterator_state:
            path.appendleft(iterator_state.state)
            iterator_state = iterator_state.previous_state_wrap

        return path
