import string

import pygame
import pygame.freetype

from ui.gui.context import settings
from ui.gui.external import ptext
from ui.gui.tools.point import Vector


class Cell:
    def __init__(self, rect: pygame.Rect, string: string):
        self.rect = rect
        self.text_rect = rect.inflate(-2 * settings.CELL_PADDING, -2 * settings.CELL_PADDING)
        self.string = string

    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(surface, settings.CELL_CONTENT_COLOR, self.rect)
        pygame.draw.rect(surface, settings.CELL_BORDER_COLOR, self.rect, 3)
        ptext.drawbox(self.string, self.text_rect, sysfontname=settings.FONT, color=settings.TEXT_COLOR)

    def get_position(self) -> Vector:
        return self.rect.left, self.rect.top

    def set_position(self, position: Vector):
        self.rect.topleft = position
        self.text_rect.topleft = position[0] + settings.CELL_PADDING, position[1] + settings.CELL_PADDING
