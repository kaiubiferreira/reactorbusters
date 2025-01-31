from assets import *
from theme import COLORS, FONT

button_x = WIDTH * 0.90 - BUTTON_WIDTH // 2
button_y = HEIGHT * 0.85
rect = pygame.Rect(button_x, button_y, BUTTON_WIDTH, BUTTON_HEIGHT)

hover_cursor = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND)
default_cursor = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW)


def basic_image_screen(image, screen, clock):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                if rect.collidepoint(mouse_pos):
                    return

        pygame.mouse.set_cursor(default_cursor)
        background_image = pygame.transform.scale(image, (WIDTH, HEIGHT))

        screen.blit(background_image, (0, 0))

        mouse_pos = pygame.mouse.get_pos()
        is_hover = rect.collidepoint(mouse_pos)

        if is_hover:
            button_color = COLORS['button_hover']
            pygame.mouse.set_cursor(hover_cursor)
        else:
            button_color = COLORS['primary']

        pygame.draw.rect(screen, button_color, rect, border_radius=BUTTON_RADIUS)
        font = pygame.font.Font(FONT, 30)
        text_surface = font.render("VOLTAR", True, COLORS['primary_text'])
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)

        pygame.display.flip()

        clock.tick(60)
