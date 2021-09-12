from typing import Optional

from algo import solution_analyzer
from ui import console, gui


def present_solution(solution: Optional[solution_analyzer.Solution]):
    if solution:
        console.present_solution(solution)
        gui.present_solution(solution)
    else:
        print("Solution not found")
