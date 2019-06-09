from objects.menus.buttons.buildmenubutton import BuildMenuButton, BuildMenu
from objects.towers.healingtower import HealingTower
import functions
import pygame


class TowerBuildButton(BuildMenuButton):
    def __init__(self, screen, build_menu: BuildMenu, slot: int, game):
        super().__init__(screen, build_menu, slot, game)
        self.active = False
        self.placements = functions.load_tower_placements('default_map')
        self.custom_hit_box = 0, 0
        self.cost = 0
        self.tower_declaration = self

    def action(self):
        self.active = not self.active
        if self.active:
            for i in range(len(self.build_menu.buttons)):
                if self.build_menu.button(i) != self:
                    self.build_menu.button(i).active = False
        self.build_menu.handle.active = False
        self.build_menu.handle.x += 100

    def place_mode(self):
        if self.active:

            for group in self.placements:
                pygame.draw.rect(self.screen, (150, 255, 150), group, 3)
            pos = pygame.mouse.get_pos()
            pos = pos[0] - self.custom_hit_box[0]/2, pos[1] - self.custom_hit_box[1]/2

            if self.try_place(pos, just_try=True):
                color_place = (0, 255, 0)
            else:
                color_place = (255, 0, 0)

            pygame.draw.rect(self.screen, color_place, (pos[0]-3, pos[1]-3,
                                                        self.custom_hit_box[0]+6,
                                                        self.custom_hit_box[1]+6))
            self.screen.blit(self.big_img, pos)

    def try_place(self, click, just_try=False):
        # pos = pos[0] - self.custom_hit_box[0]/2, pos[1] - self.custom_hit_box[1]/2

        for placement_box in self.placements:
            placement_box = pygame.rect.Rect(placement_box)
            where_tower_would_be = pygame.rect.Rect(click[0], click[1],
                                    self.custom_hit_box[0],
                                    self.custom_hit_box[1])

            if placement_box.contains(where_tower_would_be):
                for tower in self.build_menu.tower_group:
                    tower_hit_box = tower.x, tower.y,\
                                    tower.custom_hit_box[0],\
                                    tower.custom_hit_box[1]

                    if where_tower_would_be.colliderect(tower_hit_box) or self.game.gold_manager.gold < self.cost:
                        # print(f'{where_tower_would_be} collides with {tower_hit_box}')
                        return False

                if just_try:
                    return True
                self.game.gold_manager.gold -= self.cost
                tower = self.tower_declaration(click, self.game)
                tower.add(self.build_menu.tower_group)
                return True
        return False

    def _normalize_click(self, pos):
        return pos[0] - self.custom_hit_box[0]/2, pos[1] - self.custom_hit_box[1]/2





