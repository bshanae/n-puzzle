
import pygame

from algo import solution_analyzer
from ui.gui.board.board import Board
from ui.gui.context import settings

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


def present_solution(solution: solution_analyzer.Solution):
    board = Board(solution.states[0].values, solution.moves)
    animation = board.animate()

    present_solution.is_running = True

    def process_events():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                present_solution.is_running = False

    def process_drawing():
        screen.fill(settings.BACKGROUND_COLOR)
        board.draw(screen)
        pygame.display.update()

    def process_updating():
        next(animation, None)
        clock.tick(settings.FPS)

    while present_solution.is_running:
        process_events()
        process_drawing()
        process_updating()

    pygame.quit()
