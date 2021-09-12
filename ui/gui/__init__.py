from algo import solution_analyzer
from ui.gui import solution_presentation


def present_solution(solution: solution_analyzer.Solution):
    solution_presentation.init()
    solution_presentation.present_solution(solution)
