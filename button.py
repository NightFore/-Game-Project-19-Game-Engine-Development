import pygame


class Button:
    def __init__(self, x, y, width, height, label, color, font, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.label = label
        self.color = color
        self.font = font
        self.action = action

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        text_surface = self.font.render(self.label, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_hovered(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def click(self):
        if self.action:
            self.action()
