import pygame
import random
import constants
class Ground(pygame.sprite.Sprite):
    ground_level = 500

    def __init__(self, x=0, y=500):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/ground.png")
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def draw(self, window):
        pygame.draw.rect(window, (255, 255, 255), self.rect)

    def update(self, win_width):
        self.rect.x -= constants.SCROLL_SPEED
        if self.rect.x <= -win_width:
            self.kill()

class Pipes:
    width = 15
    opening = 100

    def __init__(self, win_width):
        self.x = win_width
        self.bottom_height = random.randint(10, 300)
        self.top_height = Ground.ground_level - self.bottom_height - self.opening
        self.bottom_rect, self.top_rect = pygame.Rect(0, 0, 0, 0), pygame.Rect(0, 0, 0, 0)
        self.passed = False
        self.off_screen = False

    def draw(self, window):
        self.bottom_rect = pygame.Rect(self.x, Ground.ground_level - self.bottom_height, self.width, self.bottom_height)
        pygame.draw.rect(window, (255, 255, 255), self.bottom_rect)

        self.top_rect = pygame.Rect(self.x, 0, self.width, self.top_height)
        pygame.draw.rect(window, (255, 255, 255), self.top_rect)

    def update(self):
        self.x -= constants.SCROLL_SPEED
        if self.x + Pipes.width <= 50:
            self.passed = True
        if self.x <= -self.width:
            self.off_screen = True
