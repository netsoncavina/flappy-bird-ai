import brain
import random
import pygame
import config

class Player(pygame.sprite.Sprite):
    bird_images = [pygame.image.load("assets/bird_down.png"), pygame.image.load("assets/bird_mid.png"), pygame.image.load("assets/bird_up.png")]
    def __init__(self):
        # Bird
        pygame.sprite.Sprite.__init__(self)
        self.image = Player.bird_images[0]
        self.x, self.y = 50, 200
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.image_index = 0
        self.color = random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)
        self.vel = 0
        self.flap = False
        self.alive = True
        self.lifespan = 0

        # AI
        self.decision = None
        self.vision = [0.5, 1, 0.5]
        self.fitness = 0
        self.inputs = 3
        self.brain = brain.Brain(self.inputs)
        self.brain.generate_net()

    def draw(self, window):
        window.blit(self.image, self.rect)


    def ground_collision(self, ground):
        return pygame.Rect.colliderect(self.rect, ground)

    def sky_collision(self):
        return bool(self.rect.y < 30)

    def pipe_collision(self):
        for pipe in config.pipes:
            return pygame.Rect.colliderect(self.rect, pipe.top_rect) or \
                   pygame.Rect.colliderect(self.rect, pipe.bottom_rect)

    def update(self, ground):
        if not (self.ground_collision(ground) or self.pipe_collision()):
            # Animation
            self.image_index += 1
            if self.image_index >= 30:
                self.image_index = 0
            self.image = Player.bird_images[self.image_index // 10]



            self.vel += 0.25
            self.rect.y += self.vel

            if self.vel > 5:
                self.vel = 5

            self.lifespan += 1
        else:
            self.alive = False
            self.flap = False
            self.vel = 0

    def bird_flap(self):
        if not self.flap and not self.sky_collision():
            self.flap = True
            self.vel = -5
        if self.vel >= 3:
            self.flap = False

    @staticmethod
    def closest_pipe():
        for pipe in config.pipes:
            if not pipe.passed:
                return pipe

    # AI related functions
    def look(self):
        if config.pipes:

            # Line to top pipe
            self.vision[0] = max(0, self.rect.center[1] - self.closest_pipe().top_rect.bottom) / 500
            pygame.draw.line(config.window, self.color, self.rect.center,
                             (self.rect.center[0], config.pipes[0].top_rect.bottom))

            # Line to mid pipe
            self.vision[1] = max(0, self.closest_pipe().x - self.rect.center[0]) / 500
            pygame.draw.line(config.window, self.color, self.rect.center,
                             (config.pipes[0].x, self.rect.center[1]))

            # Line to bottom pipe
            self.vision[2] = max(0, self.closest_pipe().bottom_rect.top - self.rect.center[1]) / 500
            pygame.draw.line(config.window, self.color, self.rect.center,
                             (self.rect.center[0], config.pipes[0].bottom_rect.top))

    def think(self):
        self.decision = self.brain.feed_forward(self.vision)
        if self.decision > 0.73:
            self.bird_flap()

    def calculate_fitness(self):
        self.fitness = self.lifespan

    def clone(self):
        clone = Player()
        clone.fitness = self.fitness
        clone.brain = self.brain.clone()
        clone.brain.generate_net()
        return clone

    def draw_brain(self, window):
        input_labels = ["Top Pipe", "Gap", "Bot Pipe", "Bias"]
        output_labels = ["Should Jump?"]

        ground_y = config.ground.y + 50
        screen_width = config.window.get_width()
        input_x = screen_width // 2 - 100
        output_x = screen_width // 2 + 100
        input_y_start = ground_y
        output_y = ground_y + 70

        # Draw input nodes and labels
        for i, label in enumerate(input_labels):
            y = input_y_start + i * 70  # Increased gap between circles
            pygame.draw.circle(window, (255, 255, 255), (input_x, y), 10)
            font = pygame.font.SysFont(None, 24)
            text = font.render(label, True, (255, 255, 255))
            window.blit(text, (input_x - 100, y - 10))  # Moved labels more to the left

        # Draw output node and label
        pygame.draw.circle(window, (255, 255, 255), (output_x, output_y), 10)
        font = pygame.font.SysFont(None, 24)
        text = font.render(output_labels[0], True, (255, 255, 255))
        window.blit(text, (output_x + 20, output_y - 10))

        # Draw connections
        for connection in self.brain.connections:
            from_node = connection.from_node
            to_node = connection.to_node
            color = (0, 255, 0) if connection.weight > 0 else (255, 0, 0)
            from_y = input_y_start + from_node.id * 70  # Increased gap between circles
            pygame.draw.line(window, color, (input_x, from_y), (output_x, output_y), 2)
