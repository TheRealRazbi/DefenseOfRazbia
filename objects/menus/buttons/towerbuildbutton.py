from objects.menus.buttons.buildmenubutton import BuildMenuButton, BuildMenu
from objects.towers.healingtower import HealingTower
import functions
import pygame


class TowerBuildButton(BuildMenuButton):
    def __init__(self, screen, build_menu: BuildMenu, slot: int):
        super().__init__(screen, build_menu, slot)
        self.active = False
        self.placements = functions.load_tower_placements('default_map')
        self.custom_hit_box = 0, 0

    def action(self):
        self.active = not self.active
        self.build_menu.handle.active = False
        self.build_menu.handle.x += 100

    def place_mode(self):
        if self.active:

            for group in self.placements:
                pygame.draw.rect(self.screen, (150, 255, 150), group, 3)
            pos = pygame.mouse.get_pos()
            if self.try_place(pos, just_try=True):
                color_place = (0, 255, 0)
            else:
                color_place = (255, 0, 0)



            pygame.draw.rect(self.screen, color_place, (pos[0]-3, pos[1]-3,
                                                        self.custom_hit_box[0]+6,
                                                        self.custom_hit_box[1]+6))
            self.screen.blit(self.big_img, pos)

    def try_place(self, click, just_try=False):
        for placement_box in self.placements:
            placement_box = pygame.rect.Rect(placement_box)
            where_tower_would_be = pygame.rect.Rect(click[0], click[1],
                                    self.custom_hit_box[0],
                                    self.custom_hit_box[1])
            if placement_box.contains(where_tower_would_be):
                for tower in self.build_menu.tower_group:
                    if where_tower_would_be.colliderect(tower.hit_box):
                        return False

                if just_try:
                    return True
                HealingTower(click, self.screen).add(self.build_menu.tower_group)
        return False


