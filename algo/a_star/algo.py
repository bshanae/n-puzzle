from queue import PriorityQueue
from collections import deque

from algo.a_star.state_wrap import StateWrap


class Algo:
    h_function = None
    g_function = None

    def __init__(self, h_function, g_function):
        self.h_function = h_function
        self.g_function = g_function

    def compute_f(self, start_state, current_state, target_state):
        return self.h_function(current_state, target_state) + self.g_function(start_state, current_state)

    def solve(self, start_state, target_state):
        closed_state_wraps = dict()

        start_state_wrap = StateWrap(self.compute_f(start_state, start_state, target_state), start_state)

        open_state_wraps = PriorityQueue()
        open_state_wraps.put((start_state_wrap.f_value, start_state_wrap))

        while not open_state_wraps.empty():
            f_value, current_state_wrap = open_state_wraps.get()

            if current_state_wrap.state == target_state:
                return self.restore_path(current_state_wrap)

            closed_state_wraps[current_state_wrap.state] = current_state_wrap

            for expanded_state in current_state_wrap.state.expand():
                expanded_state_wrap = StateWrap(self.compute_f(start_state, expanded_state, target_state),
                                                expanded_state,
                                                current_state_wrap)

                similar_state_wrap = closed_state_wraps.get(expanded_state, None)
                if similar_state_wrap and similar_state_wrap.f_value <= expanded_state_wrap.f_value:
                    continue

                open_state_wraps.put((expanded_state_wrap.f_value, expanded_state_wrap))

        return None

    # noinspection PyMethodMayBeStatic
    def restore_path(self, final_state):
        path = deque()

        iterator_state = final_state
        while iterator_state:
            path.appendleft(iterator_state.state)
            iterator_state = iterator_state.previous_state_wrap

        return path
