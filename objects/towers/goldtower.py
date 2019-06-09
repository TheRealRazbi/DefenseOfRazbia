from objects.projectiles.goldshot import GoldShot
from objects.towers.tower import Tower
import pygame


class GoldTower(Tower):
    cost = 25

    def __init__(self, location: tuple, game):
        super().__init__(location, game)
        self.img = pygame.image.load('lib/images/gold_tower.png')
        self.range = 125
        self.cost = 25
        self.power = 1
        self.projectile = GoldShot
        self.custom_hit_box = [50, 50]
        # self.img = pygame.transform.scale(self.img, self.custom_hit_box)
        self.scale_img()


