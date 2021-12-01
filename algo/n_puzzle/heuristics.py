from typing import Dict, Callable

from algo.n_puzzle.state import State


def manhattan(current: State, target: State) -> int:
    h_cost = 0

    for (current_row_index, current_value_index), current_value in current.enumerate():
        target_row_index, target_value_index = target.find(current_value)
        h_cost += abs(current_row_index - target_row_index) + abs(current_value_index - target_value_index)
    return h_cost


def misplaced_heuristic(current: list, target: list) -> int:
    misplaced = 0
    for cur_pos in range(len(target)):
        for next_pos in range(cur_pos + 1, len(target)):
            cur_elem = current[cur_pos]
            next_elem = current[next_pos]
            if not (target.count(cur_elem) and target.count(next_elem)):
                # here is for case of linear conflicts, index of elem may not be in a row/col
                continue
            if target.index(cur_elem) > target.index(next_elem):
                misplaced += 1
    return misplaced


def misplaced_tiles(start_state: State, target_state: State) -> bool:
    misplaced = misplaced_heuristic(start_state.listed_values, target_state.listed_values)
    zero_distance = sum(
        map(lambda x: abs(x[0] - x[1]), zip(start_state.zero_position(), target_state.zero_position()))
    )
    return (not misplaced % 2) == (not zero_distance % 2)


def linear_conflicts(current: State, target: State) -> int:
    h_cost = manhattan(current, target)
    current_cols = current.columns()
    target_cols = target.columns()
    for i in range(current.size):
        conflicts = (
            misplaced_heuristic(current.values[i], target.values[i])
            + misplaced_heuristic(current_cols[i], target_cols[i])
        )
        h_cost += conflicts
    return h_cost


def hamming(current: State, target: State) -> int:
    """exclude zero to made a heuristic admissible"""
    current_val = current.listed_values
    target_val = target.listed_values
    h_cost = 0
    for i in range(target.size * target.size):
        if current_val[i] != 0 and current_val[i] != target_val[i]:
            h_cost += 1
    return h_cost


HEURISTICS: Dict[str, Callable] = {
    'manhattan': manhattan,
    'linear': linear_conflicts,
    'hamming': hamming,
}