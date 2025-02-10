import pygame

class Ground:
    ground_level = 600

    def __init__(self, window_width):
        self.x, self.y = 0, Ground.ground_level
        self.rect = pygame.Rect(self.x, self.y, window_width, 5)

    def draw(self, window):
        pygame.draw.rect(window, (255, 255, 255), self.rect)
