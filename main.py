import functions
import game
import pygame

if __name__ == '__main__':
    size = width, height = 800, 900
    track_used = "default_map"

    wave1 = [["Grunt", 15]]
    wave2 = [["Grunt", 10], ["Grunt", 10]]

    functions.create_wave(1, wave1)
    functions.create_wave(2, wave2)


    # path = functions.load_path(also_print=True)
    # placements = functions.load_tower_placements('default_map', also_print=True)
    # placements = [[225, 115, 690, 200], [335, 320, 790, 378], [70, 203, 296, 260],
    #               [213, 260, 297, 378], [433, 201, 497, 289], [332, 233, 397, 320],
    #               [531, 232, 588, 320], [622, 201, 687, 289], [104, 296, 177, 469],
    #               [183, 413, 418, 468], [333, 411, 416, 378], [190, 80, 100, 170]]

    # path[0] = (85, 2)
    # path[1] = (85, 184)
    # path[2] = path[2]
    # path[3] = (205, 85)
    # path[4] = (706, 85)
    # path[5] = (706, 303)
    # path[7] = (607, 217)
    # path[8] = (511, 217)
    # path[9] = (511, 302)
    # path[10] = (414, 302)
    # path[11] = (414, 218)
    # path[12] = (315, 218)
    # path[13] = (315, 392)
    # path[14] = (192, 392)
    # path[15] = (192, 279)
    # path[16] = (86, 279)
    # path[17] = (86, 484)
    # path[18] = (435, 484)
    # path[19] = (435, 390)
    # path[20] = (820, 390)

    # functions.create_tower_placement(placements, 'default_map')
    # functions.create_path(path, 'default_map')


    # unit = pygame.image.load("lib/images/unit1.png")
    # unit_rect = unit.get_rect()
    # screen.blit(unit, unit_rect)

    g = game.Game(size, track_used)
    g.run()















