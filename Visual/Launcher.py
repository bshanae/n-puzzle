import pygame

from Visual.Board.Board import Board
from Visual.Context import Settings

screen: pygame.Surface


def init():
    pygame.init()
    pygame.mixer.init()

    global screen
    screen = pygame.display.set_mode((Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT))
    pygame.display.set_caption(Settings.WINDOW_TITLE)


def launch():
    values = [[22, 22, 22, 22, 22, 22],
              [22, 22, 22, 22, 22, 22],
              [22, 22, 22, 22, 22, 22],
              [22, 22, 22, 22, 22, 22],
              [22, 22, 22, 22, 22, 22],
              [22, 22, 22, 22, 22, 22]]

    board = Board(values)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(Settings.BACKGROUND_COLOR)
        board.draw(screen)

        pygame.display.flip()

    pygame.quit()
