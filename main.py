import sys

import pygame

from assets import WIDTH, HEIGHT
from credits import credits_screen
from game import game_screen
from introduction import introduction_screen
from menu import menu_screen
from resultado import resultado_screen
from rules import rules_screen

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Reactor Busters")
clock = pygame.time.Clock()

pygame.init()
running = True


def not_implemented(title, screen, clock):
    print(f'{title} Not implemented yet')


while True:
    action = menu_screen(screen, clock)

    if action == 'sair':
        pygame.quit()
        sys.exit()
    elif action == 'iniciar':
        correct_answers, go_back = game_screen(screen, clock)
        if not go_back:
            resultado_screen(correct_answers, screen, clock)
    elif action == 'créditos':
        credits_screen(screen, clock)
    elif action == 'introdução':
        introduction_screen(screen, clock)
    elif action == 'regras':
        rules_screen(screen, clock)
