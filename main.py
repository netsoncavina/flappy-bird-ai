import pygame
from sys import exit
import config
import components
import population

pygame.init()
clock = pygame.time.Clock()
population = population.Population(100)

# Images
background_image = pygame.image.load("assets/background.png")

top_pipe_image = pygame.image.load("assets/pipe_top.png")
bottom_pipe_image = pygame.image.load("assets/pipe_bottom.png")

def generate_pipes():
    config.pipes.append(components.Pipes(config.win_width))

def quit_game():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

def main():
    pipes_spawn_time = 10

    ground = pygame.sprite.Group()
    ground.add(components.Ground())

    while True:
        quit_game()

        config.window.fill((0, 0, 0))

        config.window.blit(background_image, (0, 0))

        # Spawn Ground
        if len(ground) <= 2:
            ground.add(components.Ground(config.win_width))
        ground.draw(config.window)

        # Spawn Pipes
        if pipes_spawn_time <= 0:
            generate_pipes()
            pipes_spawn_time = 200
        pipes_spawn_time -= 1

        for pipe in config.pipes:
            pipe.draw(config.window)
            pipe.update()
            if pipe.off_screen:
                config.pipes.remove(pipe)

        if not population.extinct():
            population.update_live_players()
        else:
            config.pipes.clear()
            population.natural_selection()

        ground.update(config.win_width)
        clock.tick(60)
        pygame.display.flip()

main()
