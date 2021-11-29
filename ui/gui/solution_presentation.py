
import pygame

from algo import solution_analyzer
from ui.gui.board.board import Board
from ui.gui.context import settings
from ui.gui.tools.animation_state import AnimationState

screen: pygame.Surface
clock: pygame.time.Clock


is_inited = False


def reset():
    global is_inited

    if not is_inited:
        init()
        is_inited = True


def init():
    pygame.init()
    pygame.mixer.init()

    global screen
    screen = pygame.display.set_mode((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
    pygame.display.set_caption(settings.WINDOW_TITLE)

    global clock
    clock = pygame.time.Clock()


def present_solution(solution: solution_analyzer.Solution, return_on_animation_finish: bool):
    board = Board(solution.states[0].values, solution.moves)
    animation = board.animate()

    present_solution.is_running = True

    def process_events():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)

    def process_drawing():
        screen.fill(settings.BACKGROUND_COLOR)
        board.draw(screen)
        pygame.display.update()

    def process_updating():
        animation_state = next(animation, AnimationState.UNKNOWN)
        clock.tick(settings.FPS)

        if animation_state != AnimationState.RUNNING and return_on_animation_finish:
            present_solution.is_running = False

    while present_solution.is_running:
        process_events()
        process_drawing()
        process_updating()
