class StateWrap:
    h_value: int
    g_value: int
    f_value: int
    state = None
    previous_state_wrap = None

    def __init__(self, h_value: int, g_value: int, state, previous_state=None):
        self.h_value = h_value
        self.g_value = g_value
        self.state = state
        self.previous_state_wrap = previous_state

        self.f_value = self.h_value + self.g_value

    def __lt__(self, other) -> bool:
        return self.h_value < other.h_value

    def __hash__(self) -> int:
        return hash(self.state)
