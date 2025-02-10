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
    opening = 100
    top_pipe_image = pygame.image.load("assets/pipe_top.png")
    bottom_pipe_image = pygame.image.load("assets/pipe_bottom.png")
    width = top_pipe_image.get_width()

    def __init__(self, win_width):
        self.x = win_width
        self.bottom_height = random.randint(10, 300)
        self.top_height = Ground.ground_level - self.bottom_height - self.opening

        self.bottom_rect = self.bottom_pipe_image.get_rect(topleft=(self.x, Ground.ground_level - self.bottom_height))
        self.top_rect = self.top_pipe_image.get_rect(bottomleft=(self.x, self.top_height))

        self.passed = False
        self.off_screen = False

    def draw(self, window):
        self.bottom_rect.topleft = (self.x, Ground.ground_level - self.bottom_height)
        self.top_rect.bottomleft = (self.x, self.top_height)

        window.blit(self.bottom_pipe_image, self.bottom_rect.topleft)
        window.blit(self.top_pipe_image, self.top_rect.topleft)

    def update(self):
        self.x -= constants.SCROLL_SPEED

        self.bottom_rect.x = self.x
        self.top_rect.x = self.x

        if self.x + self.width <= 50:
            self.passed = True
        if self.x <= -self.width:
            self.off_screen = True
