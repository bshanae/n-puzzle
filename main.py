from algo import n_puzzle, a_star, solution_analyzer
import ui

if __name__ == '__main__':
    start_state = n_puzzle.State([[1, 0, 2, 3],
                                  [4, 5, 6, 7],
                                  [8, 9, 10, 11],
                                  [12, 13, 14, 15]])

    target_state = n_puzzle.State([[0, 1, 3, 2],
                                   [4, 5, 6, 7],
                                   [8, 9, 10, 11],
                                   [12, 13, 14, 15]])

    algo = a_star.Algo(n_puzzle.heuristics.manhattan, n_puzzle.heuristics.manhattan)
    solution_states = algo.solve(start_state, target_state)

    solution = solution_analyzer.analyze_solution(solution_states)
    ui.present_solution(solution)
