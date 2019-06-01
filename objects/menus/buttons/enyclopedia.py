from objects.menus.buildmenu import BuildMenu
from objects.menus.buttons.buildmenubutton import BuildMenuButton
import pygame


class Encyclopedia(BuildMenuButton):
    def __init__(self, screen, build_menu: BuildMenu, slot: int):
        super().__init__(screen, build_menu, slot)
        self.img = pygame.image.load('lib/images/encyclopedia.png')
        self.rescale()

    def action(self):
        print('WORKS')