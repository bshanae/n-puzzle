from algo import solution_analyzer
from ui.gui import solution_presentation


def present_solution(solution: solution_analyzer.Solution, is_last_solution: bool):
    solution_presentation.reset()
    solution_presentation.present_solution(solution, not is_last_solution)
