import functions
from game import Game
import pygame

if __name__ == '__main__':
    size = width, height = 800, 600
    track_used = "default_map"

    path = functions.load_path(also_print=True)

    path[3] = (205, 90)
    path[4] = (706, 90)
    path[5] = (706, 303)
    path[7] = (607, 217)
    path[8] = (511, 217)
    path[9] = (511, 302)
    path[10] = (414, 302)
    path[11] = (414, 218)
    path[12] = (315, 218)
    path[13] = (315, 392)
    path[14] = (192, 392)
    path[15] = (192, 279)
    path[16] = (86, 279)
    path[17] = (86, 484)
    path[18] = (435, 484)
    path[19] = (435, 390)
    path[20] = (820, 390)


    # functions.create_path(path, 'default_map')


    unit = pygame.image.load("lib/images/unit1.png")
    unit_rect = unit.get_rect()
    # screen.blit(unit, unit_rect)

    g = Game(size, track_used)
    g.run()















