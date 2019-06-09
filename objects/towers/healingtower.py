from objects.projectiles.healingshot import HealingShot
from objects.towers.tower import Tower
import pygame
import functions


class HealingTower(Tower):
    cost = 25

    def __init__(self, location: tuple, game):
        super().__init__(location, game)
        self.img = pygame.image.load('lib/images/new_healing_tower.png')
        self.range = 125
        self.cost = 25
        self.power = 1
        self.projectile = HealingShot
        self.custom_hit_box = [50, 50]
        # self.img = pygame.transform.scale(self.img, self.custom_hit_box)
        self.scale_img()    # cost, range, power, attack_speed
        self.upgrade_menu = functions.load_tower_upgrades("HealingTower")

