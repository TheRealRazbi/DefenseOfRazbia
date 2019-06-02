import pygame
from objects.menus.buildmenu import BuildMenu
from objects.menus.buttons.towerbuildbutton import TowerBuildButton


class HealingTowerButton(TowerBuildButton):
    def __init__(self, screen, build_menu: BuildMenu, slot: int):
        super().__init__(screen, build_menu, slot)
        self.img = pygame.image.load('lib/images/new_healing_tower.png')
        # self.big_img = self.img.copy()

        self.rescale()

    def rescale(self):
        self.img = pygame.transform.scale(self.img, (39, 39))
        # self.big_img = pygame.transform.scale(self.big_img, (50, 50))