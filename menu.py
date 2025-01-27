import sys

import pygame

from assets import WIDTH, HEIGHT, MENU_BACKGROUND
from button import Button

button_radius = 20
button_width = 300
button_height = 60
button_names = ['Iniciar', 'Introdução', 'Regras', 'Créditos', 'Sair']


def menu_screen(screen, clock):
    print('menu_screen')
    background = pygame.image.load(MENU_BACKGROUND)
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    buttons = []
    for i, button_label in enumerate(button_names):
        x = (WIDTH - button_width) // 2
        y = HEIGHT - (len(button_names) - i) * (button_height + 10) - 80
        buttons.append(Button(x, y, button_width, button_height, button_label, button_radius))

    menu_running = True

    while menu_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in buttons:
                    if button.is_clicked(event.pos):
                        return button.text.lower()

        screen.blit(background, (0, 0))

        is_any_hover = False
        for button in buttons:
            button.draw(screen)
            is_any_hover = is_any_hover or button.is_hover()

        if is_any_hover:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(*pygame.cursors.arrow)

        pygame.display.update()

        clock.tick(60)  # Limit to 60 frames per second
