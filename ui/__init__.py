from typing import Optional

from algo import solution_analyzer
from ui import console, gui
from ui.console.info_storage import info


def present_solution(solution: Optional[solution_analyzer.Solution],
                     console_enabled: bool,
                     gui_enabled: bool,
                     is_last_solution: bool):
    console.present_statistics(bool(solution))
    if not solution:
        return

    if console_enabled:
        console.present_solution(solution)
    if gui_enabled:
        gui.present_solution(solution, is_last_solution)

