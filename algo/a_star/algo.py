from queue import PriorityQueue
from collections import deque

from algo.a_star.state_wrap import StateWrap


class Algo:
    h_function = None

    is_greedy = False
    is_uniform = False

    def __init__(self, h_function):
        self.h_function = h_function

    def solve(self, start_state, target_state):
        closed_state_wraps = dict()

        start_state_wrap = StateWrap(self.compute_h(start_state, target_state),
                                     self.compute_g(None),
                                     start_state)

        open_state_wraps = PriorityQueue()
        open_state_wraps.put((start_state_wrap.f_value, start_state_wrap))

        while not open_state_wraps.empty():
            f_value, current_state_wrap = open_state_wraps.get()

            if current_state_wrap.state == target_state:
                return self.restore_path(current_state_wrap)

            closed_state_wraps[current_state_wrap.state] = current_state_wrap

            for expanded_state in current_state_wrap.state.expand():
                expanded_state_wrap = StateWrap(self.compute_h(expanded_state, target_state),
                                                self.compute_g(current_state_wrap),
                                                expanded_state,
                                                current_state_wrap)

                similar_state_wrap = closed_state_wraps.get(expanded_state, None)
                if similar_state_wrap and similar_state_wrap.f_value <= expanded_state_wrap.f_value:
                    continue

                open_state_wraps.put((expanded_state_wrap.f_value, expanded_state_wrap))

        return None

    def compute_h(self, current_state, target_state):
        if self.is_uniform:
            return 0

        return self.h_function(current_state, target_state)

    def compute_g(self, previous_state):
        if self.is_greedy:
            return 0

        if previous_state is not None:
            return previous_state.g_value + 1
        else:
            return 0

    # noinspection PyMethodMayBeStatic
    def restore_path(self, final_state):
        path = deque()

        iterator_state = final_state
        while iterator_state:
            path.appendleft(iterator_state.state)
            iterator_state = iterator_state.previous_state_wrap

        return path
