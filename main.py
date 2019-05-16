import pygame
from functions import load_track, scale_size
from game import Game


if __name__ == '__main__':
    size = width, height = 800, 600
    track_used = "default_map"

    tower = pygame.image.load("lib/images/towerconcept1.png")
    # tower_rect = tower.get_rect()
    # screen.blit(tower, (tower_rect[0]+50, tower_rect[1]+500, tower_rect[2]+50, tower_rect[3]+50))

    g = Game(size, track_used)
    g.run()















