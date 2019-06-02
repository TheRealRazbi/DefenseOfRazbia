from objects.menus.buttons.buildmenubutton import BuildMenuButton, BuildMenu
from objects.towers.healingtower import HealingTower
import functions
import pygame


class TowerBuildButton(BuildMenuButton):
    def __init__(self, screen, build_menu: BuildMenu, slot: int):
        super().__init__(screen, build_menu, slot)
        self.active = False
        self.placements = functions.load_tower_placements('default_map')


    def action(self):
        self.active = not self.active
        self.build_menu.handle.active = False
        self.build_menu.handle.x += 100

    def place_mode(self):
        if self.active:

            for group in self.placements:
                pygame.draw.rect(self.screen, (150, 255, 150), group, 3)
            self.screen.blit(self.img, pygame.mouse.get_pos())


    def try_place(self, click):
        for box in self.placements:
            box = pygame.rect.Rect(box)
            if box.contains((click[0], click[1],
                            HealingTower.custom_hit_box[0],
                            HealingTower.custom_hit_box[1])):
                print("IT can be placed")
                break