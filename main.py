import pygame
import sys
from functions import build_base_track, build_unit_track, load_track, create_track, scale_size


if __name__ == '__main__':
    size = width, height = 800, 600

    unit_track = load_track(also_print=True)

    unit_track = scale_size(size, unit_track)
    # create_track([[60, 0, 90, 170], [90, 140, 190, 170], [180, 70, 210, 170],
    #               [180, 70, 620, 100], [620, 100, 590, 270]],
    #              "default_track")
    # unit_track = [[160, 70, 170, 190]]
    pygame.init()

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

















