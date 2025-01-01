import sys

import pygame

from assets import WIDTH, HEIGHT, MENU_BACKGROUND
from theme import COLORS

# Define colors
WHITE = (255, 255, 255)

# Define button properties
button_radius = 20
button_width = 300
button_height = 60
buttons = ['Iniciar', 'Introdução', 'Regras', 'Créditos', 'Sair']
button_positions = []

default_cursor = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW)
hover_cursor = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND)


def draw_button(surface, position, text, is_hover=False):
    if is_hover:
        color = COLORS['button_hover']
        pygame.mouse.set_cursor(hover_cursor)
    else:
        color = COLORS['button']

    rect = pygame.Rect(position[0], position[1], button_width, button_height)
    pygame.draw.rect(surface, color, rect, border_radius=button_radius)
    font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=rect.center)
    surface.blit(text_surface, text_rect)


# Main menu function
def menu_screen(screen, clock):
    background = pygame.image.load(MENU_BACKGROUND)
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    menu_running = True

    while menu_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Check for mouse button click
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                for index, pos in enumerate(button_positions):
                    if pos.collidepoint(mouse_pos):
                        return buttons[index].lower()

        pygame.mouse.set_cursor(default_cursor)
        screen.blit(background, (0, 0))

        # Calculate button positions
        button_positions.clear()
        for i, button in enumerate(buttons):
            x = (WIDTH - button_width) // 2  # Centered horizontally
            y = HEIGHT - (len(buttons) - i) * (button_height + 20) - 80  # Positioned towards the bottom

            # Create button rectangle
            position = pygame.Rect(x, y, button_width, button_height)
            button_positions.append(position)

            # Change color and size on hover
            mouse_pos = pygame.mouse.get_pos()
            is_hover = position.collidepoint(mouse_pos)
            draw_button(screen, position.topleft, button, is_hover)

        # Update the display
        pygame.display.flip()

        # Control the screen refresh rate
        clock.tick(60)  # Limit to 60 frames per second
