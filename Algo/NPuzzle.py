import copy
import Zobrist


def manhattan_heuristic(current, target):
    h = 0

    for (current_row_index, target_value_index), current_value in current.enumerate():
        target_row_index, target_value_index = target.find(current_value)
        h += abs(current_row_index - target_row_index) + abs(target_value_index - target_value_index)

    return h


class State:
    values = None
    hash = None

    def __init__(self, values):
        self.values = values
        self.hash = Zobrist.hash(self.values)

    def __eq__(self, other):
        return self.hash == other.hash

    def __getitem__(self, index):
        row_index, value_index = index
        return self.values[row_index][value_index]

    def __setitem__(self, index, value):
        row_index, value_index = index
        self.values[row_index][value_index] = value

    def __hash__(self):
        return self.hash

    def __str__(self):
        str = ""

        for row in self.values:
            for value in row:
                if value is not None:
                    str += ("{:2} ".format(value))
                else:
                    str += "   "

            str += "\n\r"

        return str

    def expand(self):
        def apply_offset_on_index(index):
            offsets = [(+1, 0),
                       (-1, 0),
                       (0, +1),
                       (0, -1)]

            row_index, value_index = index

            for offset_row, offset_value in offsets:
                test_index = row_index + offset_row, value_index + offset_value
                if self.is_valid_index(test_index):
                    yield test_index

        def swap(index_a, index_b):
            row_index_a, value_index_a = index_a
            row_index_b, value_index_b = index_b

            new_values = copy.deepcopy(self.values)

            temporary = new_values[row_index_a][value_index_a]
            new_values[row_index_a][value_index_a] = new_values[row_index_b][value_index_b]
            new_values[row_index_b][value_index_b] = temporary

            return State(new_values)

        for index, value in self.enumerate():
            for offset_index in apply_offset_on_index(index):
                yield swap(index, offset_index)

    cached_enumeration = None

    def enumerate(self):
        if self.cached_enumeration is None:
            self.cached_enumeration = []

            for i in range(len(self.values)):
                for j in range(len(self.values[i])):
                    self.cached_enumeration.append(((i, j), self.values[i][j]))

        return self.cached_enumeration

    def find(self, target_value):
        for (row_index, value_index), value in self.enumerate():
            if value == target_value:
                return row_index, value_index

        raise Exception(f"Value {target_value} not found")

    def is_valid_index(self, index):
        row_index, value_index = index

        if row_index < 0 or row_index >= len(self.values):
            return False

        if value_index < 0 or value_index >= len(self.values[0]):
            return False

        return True
