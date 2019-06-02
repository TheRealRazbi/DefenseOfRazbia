import pygame
from objects.menus.buildmenu import BuildMenu


class BuildMenuButton:
    def __init__(self, screen, build_menu: BuildMenu, slot: int):
        self.build_menu = build_menu
        self.screen = screen
        self.x, self.y = build_menu.slot(slot, self)
        self.img = ''
        self.big_img = ''

    def draw(self):
        self.screen.blit(self.img, (self.x, self.y))

    def rescale(self):
        self.img = pygame.transform.scale(self.img, (37, 37))

    def action(self):
        pass
