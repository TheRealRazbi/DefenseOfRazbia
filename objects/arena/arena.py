import pygame
from objects.groups.unitgroup import UnitGroup
import functions


class Arena:
    def __init__(self, screen, screen_size):
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

    def draw(self):
        self.screen.blit(self.img, (0, self.height-300))
        self.enemy_units.draw(self.screen)
        self.ally_units.draw(self.screen)

    def tp_to_arena(self, unit):
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
        self.ally_units.check_enemies()
        self.enemy_units.check_enemies()

