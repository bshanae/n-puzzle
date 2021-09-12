from algo import n_puzzle, a_star

if __name__ == '__main__':
    start_state = n_puzzle.State([[4, 2, 1],
                                  [8, 3, 6],
                                  [0, 7, 5]])

    target_state = n_puzzle.State([[0, 1, 2],
                                   [3, 4, 5],
                                   [6, 7, 8]])

    algo = a_star.Algo(n_puzzle.heuristics.manhattan, n_puzzle.heuristics.manhattan)
    path = algo.solve(start_state, target_state)

    if path:
        for state in path:
            print(state)
    else:
        print("Solution not found")
