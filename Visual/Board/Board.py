from pygame import Rect

from Visual.Context import Settings
from Visual.Board.Cell import Cell


class Board:
    cells = []

    def __init__(self, values):
        number_of_rows = len(values)
        number_of_columns = len(values[0])

        all_cells_width = (Settings.WINDOW_WIDTH - Settings.BOARD_PADDING * 2)
        cell_width = (all_cells_width - (number_of_rows + 1) * Settings.BOARD_SPACING) / number_of_rows

        all_cells_height = (Settings.WINDOW_WIDTH - Settings.BOARD_PADDING * 2)
        cell_height = (all_cells_height - (number_of_rows + 1) * Settings.BOARD_SPACING) / number_of_rows

        for row_index in range(number_of_rows):
            for column_index in range(number_of_columns):
                cell_rect = Rect(
                    Settings.BOARD_PADDING + row_index * cell_width + (row_index + 1) * Settings.BOARD_SPACING,
                    Settings.BOARD_PADDING + column_index * cell_height + (column_index + 1) * Settings.BOARD_SPACING,
                    cell_width,
                    cell_height)

                self.cells.append(Cell(cell_rect, str(values[row_index][column_index])))

    def draw(self, screen):
        for cell in self.cells:
            cell.draw(screen)
