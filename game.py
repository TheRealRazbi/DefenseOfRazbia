import functions
import pygame
import sys
from objects.units.allies.footman import Footman
from objects.units.enemies.grunt import Grunt
from objects.towers.healingtower import HealingTower
from objects.groups.unitgroup import UnitGroup
from objects.groups.projectilegroup import ProjectileGroup
from objects.menus.handle import Handle
from objects.menus.buildmenu import BuildMenu
from objects.menus.researchcentre import ResearchCentre
from objects.menus.buttons.enyclopedia import Encyclopedia
from objects.menus.buttons.healingtowerbutton import HealingTowerButton
from objects.menus.buttons.goldtowerbutton import GoldTowerButton
from objects.menus.buttons.startroundbutton import StartRoundButton
from objects.groups.towergroup import TowerGroup
from objects.arena.arena import Arena
from objects.groups.wave_control import WaveControl
from objects.groups.gold_control import GoldControl
from objects.groups.lives_control import LivesControl
from objects.menus.buttons.fastforwardbutton import FastForwardButton
from objects.menus.buttons.research.footmancount import FootmanCount
from objects.menus.buttons.research.naturalregeneration import NaturalRegeneration
import time
import asyncio


class Game:
    target_fps = 60

    def __init__(self, size: tuple, map_name: str):
        pygame.init()
        self.width = size[0]
        self.height = size[1]
        self.towers = TowerGroup()
        self.units = UnitGroup()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.map_name = map_name
        self.research_handle = Handle((0, self.height/2))
        self.research_centre = ResearchCentre(self, self.research_handle)
        self.footmen_to_spawn = 3
        self._select_track()
        self.projectiles = ProjectileGroup()
        self.wave_done = True
        self.start_button_pressed = False
        self.wave_control = WaveControl(self)
        self.start_button = StartRoundButton(self)
        self.gold_manager = GoldControl(self)
        self.lives_manager = LivesControl(self)
        self.fast_forward_button = FastForwardButton(self)
        self.fast_forward = 0

    def run(self):
        clock = pygame.time.Clock()
        run = True
        self.screen.fill((0, 0, 0))
        self._build_track()
        # self._spawn_footman()
        # self._spawn_enemies()
        self.time = time.time()

        # self._place_tower()

        while run:
            if self.fast_forward == 1:
                clock.tick(self.target_fps*2)
            elif self.fast_forward == 2:
                clock.tick(self.target_fps*3)
            else:
                clock.tick(self.target_fps)
            self._build_track()

            pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()


                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.towers.check_click(pos)

                        self._button_build_check(0, pos)
                        self._button_build_check(1, pos)
                        # self._button_build_check(0, pos, research=True)

                        self.handle.check(pos)
                        self.build_menu.check_clicks(pos)
                        self.research_centre.check_clicks(pos)
                        self.research_handle.check(pos)
                        self.start_button.check_click(pos)
                        self.fast_forward_button.check_click(pos)
                        self.fast_forward = self.fast_forward_button.pressed
                        self.start_button_pressed = self.start_button.pressed
                        # print(pos)
                    if event.button == 3:
                        self.build_menu.button(0).active = False
                        self.build_menu.button(1).active = False
                        self.towers.deselect()

                    pass

            self._button_building_frame(0, pos)
            self._button_building_frame(1, pos)


            self._main_checks()
            self.research_centre.hover(pos)
            self.start_button.draw()
            self._draw_fast_forward_button()
            self._draw_coin()
            self._draw_lives()

            pygame.display.flip()

    def _research_checks(self):
        pass

    def _spawn_footman(self):
        indent = 0
        # up_percent = int(100 * float(self.width / 600))
        for i in range(self.footmen_to_spawn):
            footman = Footman('default_map', screen_size=(self.width, self.height-300),
                              arena=self.arena)
            footman.change_start_point((footman.path[0][0], -indent))
            footman.add(self.units)
            indent += 150

    def _main_checks(self):
        self.wave_control.check()

        self.arena.check()
        self._unit_checks()
        self._tower_checks()
        self._projectile_checks()
        self._menu_checks()
        self.wave_done = self.arena.wave_done

    def _draw_fast_forward_button(self):
        self.fast_forward_button.draw()

    def _draw_coin(self):
        self.gold_manager.draw()

    def _draw_lives(self):
        self.lives_manager.draw()

    def _unit_checks(self):
        self.units.move()
        self.units.regenerate()
        self.units.draw(self.screen)

    def _tower_checks(self):
        self.towers.draw()
        self.towers.check_for_units(self.units)
        self.towers.hovering()

    def _projectile_checks(self):
        for group in self.towers.projectile_group:
            for projectile in group:
                self.projectiles.add(projectile)
        self.towers.projectile_group_empty()
        self.projectiles.update()
        self.projectiles.draw(self.screen)

    def _menu_checks(self):
        self.handle.draw(self.screen)
        self.build_menu.draw()
        self.research_handle.draw(self.screen)
        self.research_centre.draw()

    def _time_units_to_arena(self):
        if len(self.units) == 0:
            print(f'Units reached the arena in {round(time.time()-self.time, 3)} seconds')

    def _button_building_frame(self, number, pos):
        if self.build_menu.is_button_active(number):
            self.build_menu.button(number).place_mode(pos)

    def _button_build_check(self, number, pos, research=False):
        if research:
            if self.research_centre.is_button_active(number):
                if self.research_centre.button(number).try_place(self.research_centre.button(0)._normalize_click(pos)):
                    self.research_centre.button(number).active = False
        else:
            if self.build_menu.is_button_active(number):
                if self.build_menu.button(number).try_place(self.build_menu.button(0)._normalize_click(pos)):
                    self.build_menu.button(number).active = False

    def _declare_buttons(self):
        FootmanCount(self, 0)
        Encyclopedia(self.screen, self.build_menu, 2, self)
        HealingTowerButton(self.screen, self.build_menu, 0, self)
        GoldTowerButton(self.screen, self.build_menu, 1, self)
        NaturalRegeneration(self, 1)

    def _select_track(self):
        if self.map_name == '':
            raise ValueError("Track name not specified")
        # up_percent = int(100 * float(self.width / 600))

        self.track = functions.load_track(name=self.map_name)
        self.track = pygame.transform.scale(self.track, (self.width, self.height-300))
        self.arena = Arena(self.screen, (self.width, self.height), self)
        self.handle = Handle((self.width - 25, self.height / 2 - 50))
        self.build_menu = BuildMenu(screen=self.screen, handle=self.handle,
                                                 screen_size=(self.width, self.height),
                                                    tower_group=self.towers)
        self._declare_buttons()
        # self.build_menu.add()

    def _spawn_enemies(self):
        Grunt((self.width, self.height), self.arena)
        Grunt((self.width, self.height), self.arena)
        Grunt((self.width, self.height), self.arena)

    def _build_track(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.track, (0, 0))
        self.arena.draw()

    @property
    def original_map(self):
        return functions.load_track(self.map_name)