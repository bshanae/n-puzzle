import string

import pygame
import pygame.freetype

from Visual.Context import Settings
from Visual.External import ptext


class Cell:
    rect: pygame.Rect
    txt_rect: pygame.Rect
    string: string

    def __init__(self, rect: pygame.Rect, string: string):
        self.rect = rect
        self.text_rect = rect.inflate(-2 * Settings.CELL_PADDING, -2 * Settings.CELL_PADDING)

        self.string = string

    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(surface, Settings.CELL_COLOR, self.rect)
        ptext.drawbox(self.string, self.text_rect, sysfontname=Settings.FONT, color=Settings.TEXT_COLOR)
