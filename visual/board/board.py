from typing import List

from pygame import Rect

from algo.move import Move
from visual.context import settings
from visual.board.cell import Cell
from visual.tools import math
from visual.tools.point import Vector


class Board:
    cells: List[List[Cell]] = []
    moves: List[Move]

    def __init__(self, values: List[List[int]], moves: List[Move]):
        self.moves = moves

        number_of_rows = len(values)
        number_of_columns = len(values[0])

        all_cells_width = (settings.WINDOW_WIDTH - settings.BOARD_PADDING * 2)
        cell_width = (all_cells_width - (number_of_rows + 1) * settings.BOARD_SPACING) / number_of_rows

        all_cells_height = (settings.WINDOW_WIDTH - settings.BOARD_PADDING * 2)
        cell_height = (all_cells_height - (number_of_rows + 1) * settings.BOARD_SPACING) / number_of_rows

        for row_index in range(number_of_rows):
            row = []
            self.cells.append(row)

            for column_index in range(number_of_columns):
                cell_rect = Rect(
                    settings.BOARD_PADDING + row_index * cell_width + (row_index + 1) * settings.BOARD_SPACING,
                    settings.BOARD_PADDING + column_index * cell_height + (column_index + 1) * settings.BOARD_SPACING,
                    cell_width,
                    cell_height)

                row.append(Cell(cell_rect, str(values[row_index][column_index])))

    def animate(self):
        is_first_pause = True

        def get_pause_length():
            if is_first_pause:
                return settings.BOARD_ANIMATION_FIRST_PAUSE
            else:
                return settings.BOARD_ANIMATION_PAUSE

        for move in self.moves:
            for i in range(get_pause_length()):
                yield None

            for _ in self.animate_move(move):
                yield None

    def animate_move(self, move: Move):
        cell_a: Cell = self.cells[move.index_a[0]][move.index_a[1]]
        cell_b: Cell = self.cells[move.index_b[0]][move.index_b[1]]

        cell_a_position = cell_a.get_position()
        cell_b_position = cell_b.get_position()

        step_a_to_b = math.sign(cell_b_position[0] - cell_a_position[0]), math.sign(cell_b_position[1] - cell_a_position[1])
        step_b_to_a = -1 * step_a_to_b[0], -1 * step_a_to_b[1]

        cell_a.is_highlighted = True

        while True:
            a_finished = self.animate_cell(cell_a, cell_b_position, step_a_to_b)
            b_finished = self.animate_cell(cell_b, cell_a_position, step_b_to_a)

            if a_finished or b_finished:
                cell_a.is_highlighted = False
                break

            yield None

    # noinspection PyMethodMayBeStatic
    def animate_cell(self, cell: Cell, stop_position: Vector, step: Vector) -> bool:
        old_position = cell.get_position()
        new_position = old_position[0] + step[0], old_position[1] + step[1]

        cell.set_position(new_position)
        return new_position == stop_position

    def draw(self, screen):
        for row in self.cells:
            for cell in row:
                cell.draw(screen)
