import functions
from game import Game
import pygame

if __name__ == '__main__':
    size = width, height = 800, 600
    track_used = "default_map"


    path = functions.load_path(also_print=True)


    unit = pygame.image.load("lib/images/unit1.png")
    unit_rect = unit.get_rect()
    # screen.blit(unit, unit_rect)

    g = Game(size, track_used)
    g.run()















