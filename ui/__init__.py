from algo import solution_analyzer
from ui import console, gui


def present_solution(solution: solution_analyzer.Solution):
    console.present_solution(solution)
    gui.present_solution(solution)
