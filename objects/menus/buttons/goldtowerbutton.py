import pygame
from objects.menus.buildmenu import BuildMenu
from objects.menus.buttons.towerbuildbutton import TowerBuildButton
from objects.towers.goldtower import GoldTower


class GoldTowerButton(TowerBuildButton):
    def __init__(self, screen, build_menu: BuildMenu, slot: int, game):
        super().__init__(screen, build_menu, slot, game)
        self.img = pygame.image.load('lib/images/gold_tower.png')
        self.big_img = self.img.copy()
        self.custom_hit_box = 50, 50
        self.cost = GoldTower.cost
        self.rescale()
        self.tower_declaration = GoldTower

    def rescale(self):
        self.img = pygame.transform.scale(self.img, (39, 39))
        self.big_img = pygame.transform.scale(self.big_img, (50, 50))