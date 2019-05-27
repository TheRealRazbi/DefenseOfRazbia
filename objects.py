import pygame
import functions
import time, math


class UnitGroup(pygame.sprite.Group):
    def __init__(self, *args):
        super().__init__(*args)

    def move(self):
        for sprite in self.sprites():
            sprite.move()

    def draw(self, screen):
        for sprite in self.sprites():
            sprite.draw(screen)









class Entity(pygame.sprite.Sprite):
    entities = 0

    def __init__(self):
        super().__init__()
        Entity.entities += 1
        self.position = 0, 0

    @classmethod
    def hm_entities(cls):
        return cls.entities


class Unit(Entity):
    def __init__(self, map_name, screen_size):
        super().__init__()
        self.path = functions.load_path(map_name, scaling=screen_size)
        self.x = self.path[0][0]
        self.y = self.path[0][1]
        self.x_ratio = screen_size[0] / 800
        self.y_ratio = screen_size[1] / 600
        self.prev_x = self.x
        self.prev_y = self.y
        self.move_point = 0
        self.movement_speed = 2 * ((self.x_ratio + self.y_ratio)/2)
        self.img = ''
        self.angle_change = 0
        self.custom_hit_box = [0, 0]
        self.rect = (0, 0)
        self._facing = 'e'
        self.moveable = True
        self.choose_facing = True

    def change_start_point(self, where: tuple):
        self.path.insert(0, (where[0], where[1]))
        self.x = self.path[0][0]
        self.y = self.path[0][1]
        self.move_point = 0



    def scale_img(self):
        size = int(50 * self.x_ratio), int(50 * self.y_ratio)
        self.img = pygame.transform.scale(self.img, size)

    @property
    def hit_box(self):
        return self.centred[0], self.centred[1],\
                self.centred[0]+self.custom_hit_box[0],\
                self.centred[1]+self.custom_hit_box[1]

    @property
    def facing(self):
        return self._facing

    @property
    def angle_change(self):
        return self._angle

    @angle_change.setter
    def angle_change(self, angle):
        self._angle = angle



    @angle_change.setter
    def angle_change(self, angle):
        self._angle = angle

    def _change_direction(self, start, end):
        if start[0] == end[0]:
            # print(f'[0]{start[0]} equals to {end[0]}')
            if start[1] > end[1]:
                self.facing = 's'
            elif start[1] < end[1]:
                self.facing = 'n'
        elif start[1] == end[1]:
            # print(f'[1]{start[1]} equals to {end[1]}')
            if start[0] > end[0]:
                self.facing = 'w'
            elif start[0] < end[0]:
                self.facing = 'e'


    def move(self):
        if self.moveable:
            start = self.path[self.move_point]
            end = self.path[self.move_point+1]

            corner = False

            moving = self.movement_speed
            if self.choose_facing:
                self._change_direction(start, end)
                self.choose_facing = False

            if start[0] == end[0]:
                if start[1] > end[1]:
                    if self.y - moving <= end[1]:
                        moving = end[1] - self.y
                        corner = True
                    self.y -= moving

                elif start[1] < end[1]:
                    if self.y + moving >= end[1]:
                        moving = end[1] - self.y
                        corner = True

                    self.y += moving

            elif start[1] == end[1]:
                if start[0] > end[0]:
                    if self.x - moving <= end[0]:
                        moving = end[0] - self.x
                        corner = True


                    self.x -= moving

                elif start[0] < end[0]:
                    if self.x + moving >= end[0]:
                        moving = end[0] - self.x
                        corner = True

                    self.x += moving

            try:
                if corner:
                    self.move_point += 1
                    start = self.path[self.move_point]
                    end = self.path[self.move_point + 1]
                    self._change_direction(start, end)
            except IndexError as e:
                # print(e)
                # print('REE1')
                self.moveable = False
                self.tp_to_arena()


    def tp_to_arena(self):
        self.kill()

    def draw(self, screen):
        screen.blit(self.img, (self.hit_box[0], self.hit_box[1]))

    @property
    def centred(self):
        return self.x-self.custom_hit_box[0]/2, self.y-self.custom_hit_box[1]/2

    @facing.setter
    def facing(self, direction):
        directions = {'n': 0, 'e': 90, 's': 180, 'w': 270}
        self.angle_change = directions[direction] - directions[self.facing]
        if self.angle_change > 180:
            self.angle_change -= 360
        if self.angle_change < -180:
            self.angle_change += 360

        self.img = pygame.transform.rotate(self.img, self.angle_change)
        self.angle_change = 0

        self._facing = direction



class Ally(Unit):
    def __init__(self, map_name, screen_size):
        super().__init__(map_name, screen_size)

    # def tp_to_arena(self):
    #     pass

class Enemy(Unit):
    pass


class Footman(Ally):
    def __init__(self, map_name, screen_size):
        super().__init__(map_name, screen_size)
        self.img = pygame.image.load('lib/images/footman.png')
        self.custom_hit_box = 50, 30  # for scale 50, 50
        self.scale_img()


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
        self.target_screen = target_screen
        self.selected = True
        self.cooldown = 0

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
                    print('shoot')
                else:
                    self.cooldown -= 1
                    print('reloading')
                pass
            else:
                # print(f'{unit} with coordonates {unit.centred[0]} {unit.centred[1]} and distance {int(distance)}'
                #       f' x_change = {unit.x - self.middle[0]} y_change = {unit.y + self.middle[1]}')
                pass
            # print(distance)
            pass

    def draw(self, screen):
        # screen.blit(self.img, (self.hit_box[0], self.hit_box[1]))
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
        self.x = self.x
        self.y = self.y

    @property
    def middle(self):
        return self.x + self.custom_hit_box[0]/2, self.y + self.custom_hit_box[1]/2


class HealingTower(Tower):
    def __init__(self, location: tuple, target_screen=None):
        super().__init__(location, target_screen=target_screen)
        self.img = pygame.image.load('lib/images/healing_tower.png')
        self.cost = 10
        self.range = 175
        self.custom_hit_box = [50, 50]

        print(self.middle)
        self.scale_img()
        print(self.middle)


class Projectile:
    def __init__(self, target):
        pass


class HealingShot(Projectile):
    def __init__(self, target):
        super().__init__(target)



class Button:
    def __init__(self, location: tuple):
        self.x = location[0]
        self.y = location[1]
        self.custom_hit_box = self.x, self.y, self.x + 0, self.y + 0



class BuildMenu:
    def __init__(self):
        pass





if __name__ == '__main__':
    pass










