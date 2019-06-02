import pygame
import math
from objects.projectiles.healingshot import HealingShot


class Tower(pygame.sprite.Sprite):
    tower_size = 0, 0
    towers = []

    def __init__(self, location: tuple, target_screen=None):
        super().__init__()
        self.x = location[0]
        self.y = location[1]
        self.custom_hit_box = [0, 0]
        self.damage = 0
        self.range = 0
        self.img = ''
        self.cost = 0
        self.power = 0
        self.target_screen = target_screen
        self.selected = True
        self.cooldown = 0
        self.projectile_group = pygame.sprite.Group()
        self.projectile = ''

    def check_for_units(self, group):
        if self.selected:
            pygame.draw.circle(self.target_screen, (0, 0, 0), (int(self.middle[0]), int(self.middle[1])),
                               self.range, 5)
        for unit in group:
            distance = math.sqrt(abs(unit.x - self.middle[0])**2 + abs(unit.y - self.middle[1])**2)

            if distance <= self.range:
                # print(f'{unit} is inside the tower range')
                if self.cooldown <= 0:
                    self.cooldown = 40
                    if self.projectile == HealingShot and unit.hp == unit.max_hp:
                        pass
                    else:
                        projectile = self.projectile(self.middle, unit, self.power)
                        self.projectile_group.add(projectile)
                        # print(f"SHOT {unit}")
                        break
                else:
                    self.cooldown -= 1
                    break

    def draw(self, screen):
        screen.blit(self.img, (self.x, self.y))

    @property
    def hit_box(self):
        return self.centred[0], self.centred[1],\
                self.centred[0]+self.custom_hit_box[0],\
                self.centred[1]+self.custom_hit_box[1]

    @property
    def centred(self):
        return self.x-self.custom_hit_box[0]/2, self.y-self.custom_hit_box[1]/2

    def scale_img(self):
        self.img = pygame.transform.scale(self.img, (50, 50))
        # self.x = self.x
        # self.y = self.y

    @property
    def middle(self):
        return self.x + self.custom_hit_box[0]/2, self.y + self.custom_hit_box[1]/2
