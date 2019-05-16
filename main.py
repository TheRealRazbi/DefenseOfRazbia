import pygame
from functions import build_base_track, build_unit_track, load_track, create_track, scale_size
from game import Game


if __name__ == '__main__':
    size = width, height = 800, 600
    track_used = "first_track_completed"

    unit_track = load_track(also_print=True, name=track_used)
    unit_track = scale_size(size, unit_track)

    # pygame.init()

    black = 0, 0, 0

    screen = pygame.display.set_mode(size)

    tower = pygame.image.load("lib/images/towerconcept1.png")
    tower_rect = tower.get_rect()

    screen.fill(black)
    build_base_track(size, screen)
    build_unit_track(unit_track, screen)
    # screen.blit(tower, (tower_rect[0]+50, tower_rect[1]+500, tower_rect[2]+50, tower_rect[3]+50))

    game = Game(size)
    game.run()















