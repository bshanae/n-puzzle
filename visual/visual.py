from typing import List

import pygame

from algo.move import Move
from visual.context import settings

screen: pygame.Surface
clock: pygame.time.Clock


def init():
    pygame.init()
    pygame.mixer.init()

    global screen
    screen = pygame.display.set_mode((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
    pygame.display.set_caption(settings.WINDOW_TITLE)

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
        screen.fill(settings.BACKGROUND_COLOR)
        board.draw(screen)
        pygame.display.update()

    def process_updating():
        next(animation, None)
        clock.tick(settings.FPS)

    while visualise.is_running:
        process_events()
        process_drawing()
        process_updating()

    pygame.quit()
