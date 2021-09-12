class StateWrap:
    f_value: int
    state = None
    previous_state_wrap = None

    def __init__(self, f_value: int, state, previous_state=None):
        self.f_value = f_value
        self.state = state
        self.previous_state_wrap = previous_state

    def __lt__(self, other) -> bool:
        return self.f_value < other.f_value

    def __hash__(self) -> int:
        return hash(self.state)
