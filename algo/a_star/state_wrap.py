from typing import Optional

from algo.n_puzzle import State


class StateWrap:

    def __init__(
        self,
        h_value: int,
        g_value: int,
        state: State,
        previous_state: Optional[State] = None,
    ):
        self.h_value = h_value
        self.g_value = g_value
        self.f_value: int = self.h_value + self.g_value
        self.state = state
        self.previous_state_wrap = previous_state

    def __lt__(self, other) -> bool:
        return self.h_value < other.h_value

    def __hash__(self) -> int:
        return hash(self.state)


