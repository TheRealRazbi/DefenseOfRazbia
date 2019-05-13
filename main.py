import pygame
import sys
from functions import build_base_track, build_unit_track, load_track


if __name__ == '__main__':

    unit_track = load_track(also_print=True)
    pygame.init()

    size = width, height = 800, 600
    black = 0, 0, 0

    screen = pygame.display.set_mode(size)

    tower = pygame.image.load("lib/images/towerconcept1.png")
    tower_rect = tower.get_rect()

    screen.fill(black)
    build_base_track(size, screen)
    build_unit_track(unit_track, screen)
    screen.blit(tower, (tower_rect[0]+50, tower_rect[1]+500, tower_rect[2]+50, tower_rect[3]+50))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        pygame.display.flip()

















