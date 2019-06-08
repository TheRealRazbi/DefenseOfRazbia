from objects.units.ally import Ally
import pygame
import os


class Footman(Ally):
    def __init__(self, map_name, screen_size, arena):
        super().__init__(map_name, screen_size, arena)
        self.walking_animation = True
        self.img = pygame.image.load('lib/images/new_footman.png')
        self.img_stand = pygame.image.load('lib/images/footman/standing.png')
        self.load_animation()
        # self.hp = self.max_hp

        self.custom_hit_box = 50, 30  # for scale 50, 50
        self.scale_img()


    def load_animation(self):
        files_found = 0
        for filename in os.listdir('lib/images/footman'):
            if filename.startswith("move"):
                files_found += 1
        for image in range(files_found):
            self.img_move.append(pygame.image.load(f'lib/images/footman/move{image}.png'))











