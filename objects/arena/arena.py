import pygame
from objects.groups.unitgroup import UnitGroup
import functions


class Arena:
    def __init__(self, screen, screen_size, game_object):
        self.game = game_object
        self.width, self.height = screen_size
        self.img = pygame.image.load('lib/images/arena.png')
        self.screen = screen
        self.ally_units = UnitGroup()
        self.enemy_units = UnitGroup()
        self.hit_box = 0, self.height-300, self.width, self.height
        self.ally_target_x = 50
        self.ally_target_y = self.height - 60
        self.enemy_target_x = self.width - 50
        self.enemy_target_y = self.height - 60
        self.waiting = True
        self.check_point = [[self.width-100, self.height-150], [100, self.height-150]]
        self.wave_done = True

    def draw(self):
        self.screen.blit(self.img, (0, self.height-300))
        self.enemy_units.draw(self.screen)
        self.ally_units.draw(self.screen)

    def tp_to_arena(self, unit):
        self.wave_done = False
        if unit.team == 0:

            while not functions.clicked_in_a_box(self.hit_box, (self.ally_target_x, self.ally_target_y)):
                if self.ally_target_y < self.height - 300:
                    self.ally_target_y += 300
                    self.ally_target_x += 50
            else:
                unit.x, unit.y = self.ally_target_x, self.ally_target_y
                self.ally_target_y -= 75

        elif unit.team == 1:
            print('enemy placed')
            while not functions.clicked_in_a_box(self.hit_box, (self.enemy_target_x, self.enemy_target_y)):
                if self.enemy_target_y < self.height - 300:
                    self.enemy_target_y += 300
                    self.enemy_target_x -= 50
            else:
                unit.x, unit.y = self.enemy_target_x, self.enemy_target_y
                self.enemy_target_y -= 75

        elif unit.team == -1:
            raise ValueError("No valid team")

    def check(self):
        if len(self.ally_units) == self.game.footmen_to_spawn or not self.waiting:
            if self.waiting:
                self._init_all_units()
                self.waiting = False
                pygame.display.flip()
                print('waiting to engage')
                pygame.time.wait(1000)
                print('engaging')
            else:
                self.all_units.attack_move()
        # self.ally_units.check_enemies()
        # self.enemy_units.check_enemies()

    def _init_all_units(self):
        self._all_units = UnitGroup()
        for unit in self.ally_units:
            self._all_units.add(unit)
        for unit in self.enemy_units:
            self._all_units.add(unit)

    @property
    def all_units(self):
        return self._all_units

    def clear(self):
        self.all_units.empty()
        self.enemy_units.empty()
        self.ally_units.empty()
        self.waiting = True
        self.ally_target_x = 50
        self.ally_target_y = self.height - 60
        self.enemy_target_x = self.width - 50
        self.enemy_target_y = self.height - 60








