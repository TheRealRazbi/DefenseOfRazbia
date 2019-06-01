from objects.units.ally import Ally
import pygame


class Footman(Ally):
    def __init__(self, map_name, screen_size):
        super().__init__(map_name, screen_size)
        self.img = pygame.image.load('lib/images/new_footman.png')
        self.custom_hit_box = 50, 30  # for scale 50, 50
        self.scale_img()
