import functions
import pygame
import sys
from objects.units.allies.footman import Footman
from objects.towers.healingtower import HealingTower
from objects.groups.unitgroup import UnitGroup
from objects.groups.projectilegroup import ProjectileGroup
from objects.menus.handle import Handle
from objects.menus.buildmenu import BuildMenu
from objects.menus.buttons.enyclopedia import Encyclopedia
from objects.menus.buttons.healingtowerbutton import HealingTowerButton
from objects.groups.towergroup import TowerGroup
from objects.arena.arena import Arena


class Game:
    def __init__(self, size: tuple, map_name: str):
        pygame.init()
        self.width = size[0]
        self.height = size[1]
        self.towers = TowerGroup()
        self.units = UnitGroup()
        self.arena_units = UnitGroup()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.map_name = map_name
        self._select_track()
        self.projectiles = ProjectileGroup()


    def run(self):
        run = True
        clock = pygame.time.Clock()
        self.screen.fill((0, 0, 0))
        self._build_track()
        self._spawn_footman()
        # self._place_tower()

        while run:

            clock.tick(60)
            self._build_track()

            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()


                pos = pygame.mouse.get_pos()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.towers.check_click(pos)
                        if self.build_menu.is_button_active(0):
                            if self.build_menu.button(0).try_place(self.build_menu.button(0)._normalize_click(pos)):
                                self.build_menu.button(0).active = False

                        self.handle.check(pos)
                        self.build_menu.check_clicks(pos)
                        # print(pos)
                    if event.button == 3:
                        self.build_menu.button(0).active = False
                        self.towers.deselect()

                    pass

            if self.build_menu.is_button_active(0):
                self.build_menu.button(0).place_mode()

            self.units.move()
            self.units.draw(self.screen)
            self.towers.draw(self.screen)

            self.towers.check_for_units(self.units)

            for group in self.towers.projectile_group:
                for projectile in group:
                    self.projectiles.add(projectile)
            self.towers.projectile_group_empty()
            self.projectiles.update()
            self.projectiles.draw(self.screen)

            self.handle.draw(self.screen)
            self.build_menu.draw()
            # print(self.units)

            pygame.display.flip()

    def _spawn_footman(self):
        indent = 0
        # up_percent = int(100 * float(self.width / 600))
        for i in range(10):
            footman = Footman('default_map', screen_size=(self.width, self.height-300))
            footman.change_start_point((footman.path[0][0], -indent))
            footman.add(self.units)
            indent += 150

    def _place_tower(self):
        HealingTower((250, 250), self.screen).add(self.towers)




    def _select_track(self):
        if self.map_name == '':
            raise ValueError("Track name not specified")
        # up_percent = int(100 * float(self.width / 600))

        self.track = functions.load_track(name=self.map_name)
        self.track = pygame.transform.scale(self.track, (self.width, self.height-300))
        self.arena = Arena(self.screen, (self.width, self.height), self.arena_units)
        self.handle = Handle((self.width - 25, self.height / 2 - 50))
        self.build_menu = BuildMenu(screen=self.screen, handle=self.handle,
                                                 screen_size=(self.width, self.height),
                                                    tower_group=self.towers)
        Encyclopedia(self.screen, self.build_menu, 1)
        HealingTowerButton(self.screen, self.build_menu, 0)
        # self.build_menu.add()

    def _build_track(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.track, (0, 0))
        self.arena.draw()

    @property
    def original_map(self):
        return functions.load_track(self.map_name)