import sys

import pygame

from assets import screen, clock
from credits import credits_screen
from game import game_screen
from introduction import introduction_screen
from menu import menu_screen
from results import results_screen
from rules import rules_screen

pygame.init()
running = True

while True:
    action = menu_screen(screen, clock)

    if action == 'sair':
        pygame.quit()
        sys.exit()
    elif action == 'iniciar':
        correct_answers, go_back = game_screen(screen, clock)
        if not go_back:
            results_screen(correct_answers, screen, clock)
    elif action == 'créditos':
        credits_screen(screen, clock)
    elif action == 'introdução':
        introduction_screen(screen, clock)
    elif action == 'regras':
        rules_screen(screen, clock)
