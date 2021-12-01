import copy
from typing import Dict, Callable

from algo.n_puzzle.state import State
from reader.constants import PUZZLE_MAP_TYPE


def manhattan(current: State, target: State) -> int:
    h_cost = 0

    for (current_row_index, current_value_index), current_value in current.enumerate():
        target_row_index, target_value_index = target.find(current_value)
        h_cost += abs(current_row_index - target_row_index) + abs(current_value_index - target_value_index)
    return h_cost


def misplaced_one_swap(current: PUZZLE_MAP_TYPE, target: PUZZLE_MAP_TYPE) -> bool:
    misplaced = []
    for row in range(len(current)):
        for col in range(len(current[row])):
            cur_elem = current[row][col]
            target_elem = target[row][col]
            if cur_elem != target_elem:
                misplaced.append((cur_elem, row, col))

    if len(misplaced) == 2:
        tmp_values = copy.deepcopy(current)
        first, second = misplaced
        tmp_values[first[1]][first[2]] = second[0]
        tmp_values[second[1]][second[2]] = first[0]
        if tmp_values == target:
            return True
    return False


def misplaced_heuristic(current: PUZZLE_MAP_TYPE, target: PUZZLE_MAP_TYPE) -> int:
    misplaced = 0
    if misplaced_one_swap(current, target):
        return 1
    current_listed = sum(current, [])
    target_listed = sum(target, [])

    for cur_pos in range(len(target_listed)):
        for next_pos in range(cur_pos + 1, len(target_listed)):
            cur_elem = current_listed[cur_pos]
            next_elem = current_listed[next_pos]
            if not (target_listed.count(cur_elem) and target_listed.count(next_elem)):
                continue

            if target_listed.index(cur_elem) > target_listed.index(next_elem):
                misplaced += 1

    return misplaced


def misplaced_tiles(start_state: State, target_state: State) -> bool:
    misplaced = misplaced_heuristic(start_state.values, target_state.values)
    zero_distance = sum(
        map(lambda x: abs(x[0] - x[1]), zip(start_state.zero_position(), target_state.zero_position()))
    )
    if misplaced == 1 and zero_distance == 0:
        return True
    return (not misplaced % 2) == (not zero_distance % 2)


def linear_conflicts(current: State, target: State) -> int:
    h_cost = manhattan(current, target)
    current_cols = current.columns()
    target_cols = target.columns()
    for i in range(current.size):
        conflicts = (
            misplaced_heuristic([current.values[i]], [target.values[i]])
            + misplaced_heuristic([current_cols[i]], [target_cols[i]])
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