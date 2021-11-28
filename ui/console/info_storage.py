
class Info:
    def __init__(self):
        self.algo: str = ''
        self.h_function: str = ''
        self.greedy: bool = False
        self.uniform: bool = False
        self.puzzle_size: int = 0
        self.start_state: list = []
        self.target_state: list = []
        self.solution_type: str = ''
        self.max_rss: int = 0
        self.time_complexity: int = 0
        self.size_complexity: int = 0
        self.duration: float = 0.0
        self.moves_ct: int = 0


info = Info()
