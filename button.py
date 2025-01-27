# Button class
import pygame

from theme import COLORS


class Button:
    def __init__(self, x, y, width, height, text, radius, font_size=36):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.Font(None, font_size)
        self.radius = radius

    def draw(self, surface):
        color = COLORS['button_hover'] if self.rect.collidepoint(pygame.mouse.get_pos()) else COLORS['button']
        pygame.draw.rect(surface, color, self.rect, border_radius=self.radius)

        text_surface = self.font.render(self.text, True, COLORS['button_text'])
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

    def is_hover(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())
