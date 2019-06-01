from objects.projectiles.healingshot import HealingShot
from objects.towers.tower import Tower
import pygame


class HealingTower(Tower):
    def __init__(self, location: tuple, target_screen=None):
        super().__init__(location, target_screen=target_screen)
        self.img = pygame.image.load('lib/images/new_healing_tower.png')
        self.cost = 10
        self.range = 175
        self.custom_hit_box = [50, 50]
        self.power = 5
        self.projectile = HealingShot
        self.scale_img()

