from queue import PriorityQueue
from collections import deque


class State:
    raw_state = None
    f_value = None
    previous_state = None

    def __init__(self, raw_state, f_value, previous_state=None):
        self.raw_state = raw_state
        self.f_value = f_value
        self.previous_state = previous_state

    def __lt__(self, other):
        return self.f_value < other.f_value

    def __hash__(self):
        return hash(self.raw_state)


class AStar:
    h_function = None
    g_function = None

    def __init__(self, h_function, g_function):
        self.h_function = h_function
        self.g_function = g_function

    def f_function(self, start_state, current_state, target_state):
        return self.h_function(current_state, target_state) + self.g_function(start_state, current_state)

    def solve(self, raw_start_state, raw_target_state):
        closed_states = dict()

        start_state = State(raw_start_state, self.f_function(raw_start_state, raw_start_state, raw_target_state))

        open_states = PriorityQueue()
        open_states.put((start_state.f_value, start_state))

        while not open_states.empty():
            f_value, current_state = open_states.get()

            if current_state.raw_state == raw_target_state:
                return self.restore_path(current_state)

            closed_states[current_state.raw_state] = current_state

            for raw_expanded_state in current_state.raw_state.expand():
                expanded_state = State(raw_expanded_state,
                                       self.f_function(raw_start_state, raw_expanded_state, raw_target_state),
                                       current_state)

                similar_state = closed_states.get(raw_expanded_state, None)
                if similar_state and similar_state.f_value <= expanded_state.f_value:
                    continue

                open_states.put((expanded_state.f_value, expanded_state))

        return None

    def restore_path(self, final_state):
        path = deque()

        iterator_state = final_state
        while iterator_state:
            path.appendleft(iterator_state.raw_state)
            iterator_state = iterator_state.previous_state

        return path