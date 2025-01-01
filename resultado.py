from assets import *
from theme import COLORS

button_x = WIDTH * 0.5
button_y = HEIGHT * 0.9
rect = pygame.Rect(button_x, button_y, BUTTON_WIDTH, BUTTON_HEIGHT)


def resultado_screen(resultado, screen, clock):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                if rect.collidepoint(mouse_pos):
                    return
        screen.fill((255, 255, 255))  # RGB for white

        if resultado > 3:
            background_image = SUCCESS_IMAGE
        else:
            background_image = FAILURE_IMAGE

        screen.blit(background_image, (0, 0))

        mouse_pos = pygame.mouse.get_pos()
        is_hover = rect.collidepoint(mouse_pos)

        if is_hover:
            button_color = COLORS['button_hover']
        else:
            button_color = COLORS['primary']

        pygame.draw.rect(screen, button_color, rect, border_radius=BUTTON_RADIUS)
        font = pygame.font.Font(None, 36)
        text_surface = font.render("Voltar", True, COLORS['primary_text'])
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)

        pygame.display.flip()

        clock.tick(60)
