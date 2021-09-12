from algo.n_puzzle import State


def manhattan(current: State, target: State):
    h = 0

    for (current_row_index, target_value_index), current_value in current.enumerate():
        target_row_index, target_value_index = target.find(current_value)
        h += abs(current_row_index - target_row_index) + abs(target_value_index - target_value_index)

    return h
