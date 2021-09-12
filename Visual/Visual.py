from typing import List

import pygame

from Algo.Move import Move
from Visual.Board.Board import Board
from Visual.Context import Settings

screen: pygame.Surface
clock: pygame.time.Clock


def init():
    pygame.init()
    pygame.mixer.init()

    global screen
    screen = pygame.display.set_mode((Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT))
    pygame.display.set_caption(Settings.WINDOW_TITLE)

    global clock
    clock = pygame.time.Clock()


def visualise(values: List[List[int]], moves: List[Move]):
    board = Board(values, moves)
    animation = board.animate()

    visualise.is_running = True

    def process_events():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                visualise.is_running = False

    def process_drawing():
        screen.fill(Settings.BACKGROUND_COLOR)
        board.draw(screen)
        pygame.display.update()

    def process_updating():
        next(animation, None)
        clock.tick(Settings.FPS)

    while visualise.is_running:
        process_events()
        process_drawing()
        process_updating()

    pygame.quit()
