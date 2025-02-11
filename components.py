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

import pygame
import random
import constants

class Pipes:
    opening = 125
    top_pipe_image = pygame.image.load("assets/pipe_top.png")
    bottom_pipe_image = pygame.image.load("assets/pipe_bottom.png")
    width = top_pipe_image.get_width()

    hitbox_padding_x = 10
    hitbox_padding_y = 10

    def __init__(self, win_width):
        self.x = win_width
        self.bottom_height = random.randint(10, 300)
        self.top_height = Ground.ground_level - self.bottom_height - self.opening

        self.bottom_rect = self.bottom_pipe_image.get_rect(topleft=(self.x, Ground.ground_level - self.bottom_height))
        self.top_rect = self.top_pipe_image.get_rect(bottomleft=(self.x, self.top_height))

        self.bottom_hitbox = pygame.Rect(
            self.bottom_rect.x + self.hitbox_padding_x,
            self.bottom_rect.y + self.hitbox_padding_y,
            self.bottom_rect.width - (2 * self.hitbox_padding_x),
            self.bottom_rect.height - (2 * self.hitbox_padding_y)
        )

        self.top_hitbox = pygame.Rect(
            self.top_rect.x + self.hitbox_padding_x,
            self.top_rect.y + self.hitbox_padding_y,
            self.top_rect.width - (2 * self.hitbox_padding_x),
            self.top_rect.height - (2 * self.hitbox_padding_y)
        )

        self.passed = False
        self.off_screen = False

    def draw(self, window):
        self.bottom_rect.topleft = (self.x, Ground.ground_level - self.bottom_height)
        self.top_rect.bottomleft = (self.x, self.top_height)

        window.blit(self.bottom_pipe_image, self.bottom_rect.topleft)
        window.blit(self.top_pipe_image, self.top_rect.topleft)

        pygame.draw.rect(window, (255, 0, 0), self.bottom_hitbox, 2)
        pygame.draw.rect(window, (255, 0, 0), self.top_hitbox, 2)

    def update(self):
        self.x -= constants.SCROLL_SPEED

        self.bottom_rect.x = self.x
        self.top_rect.x = self.x

        self.bottom_hitbox.x = self.bottom_rect.x + self.hitbox_padding_x
        self.bottom_hitbox.y = self.bottom_rect.y + self.hitbox_padding_y
        self.top_hitbox.x = self.top_rect.x + self.hitbox_padding_x
        self.top_hitbox.y = self.top_rect.y + self.hitbox_padding_y

        if self.x + self.width <= 50:
            self.passed = True
        if self.x <= -self.width:
            self.off_screen = True
