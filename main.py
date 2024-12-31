import sys
from functools import partial

import pygame

from assets import WIDTH, HEIGHT
from credits import credits_screen
from game import game_screen
from menu import menu_screen
from resultado import resultado_screen

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Reactor Busters")
clock = pygame.time.Clock()

pygame.init()
running = True


def not_implemented(title, screen, clock):
    print(f'{title} Not implemented yet')


screens = {
    'menu': menu_screen,
    'regras': partial(not_implemented, "regras"),
    'créditos': credits_screen,
    'introdução': partial(not_implemented, "intro"),
    'iniciar': game_screen,
}

while True:
    action = menu_screen(screen, clock)
    print(action)

    if action == 'sair':
        pygame.quit()
        sys.exit()
    elif action == 'iniciar':
        correct_answers = game_screen(screen, clock)
        resultado_screen(correct_answers, screen, clock)
