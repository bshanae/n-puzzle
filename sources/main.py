import AStar
import NPuzzle

if __name__ == '__main__':
    start_state = NPuzzle.State([[4, 2, 1],
                                 [8, 3, 6],
                                 [0, 7, 5]])

    target_state = NPuzzle.State([[0, 1, 2],
                                  [3, 4, 5],
                                  [6, 7, 8]])

    a_star = AStar.AStar(NPuzzle.manhattan_heuristic, NPuzzle.manhattan_heuristic)
    path = a_star.solve(start_state, target_state)

    if path:
        for state in path:
            print(state)
    else:
        print("Solution not found")
