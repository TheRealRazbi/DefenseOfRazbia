import pygame
import functions
import time, math


class ProjectileGroup(pygame.sprite.Group):
    def __init__(self, *args):
        super().__init__(*args)

    def draw(self, screen):
        for sprite in self.sprites():
            sprite.draw(screen)





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
        self.max_hp = 100
        self.hp = 1
        self._facing = 'e'
        self.moveable = True
        self.choose_facing = True

    def hit(self, power_type, power):
        if power_type == 'HEAL':
            if self.hp < self.max_hp:
                self.hp += power
                if self.hp > self.max_hp:
                    self.hp = self.max_hp


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
        hp_percent = (30 * (self.hp / self.max_hp)) - 15
        screen.blit(self.img, (self.hit_box[0], self.hit_box[1]))
        pygame.draw.line(screen, (255, 255, 255), (self.x-15, self.centred[1]+self.custom_hit_box[1]+30),
                                            (self.x+15, self.centred[1]+self.custom_hit_box[1]+30), 5)

        pygame.draw.line(screen, (0, 255, 0), (self.x-15, self.centred[1]+self.custom_hit_box[1]+30),
                                            (self.x+hp_percent, self.centred[1]+self.custom_hit_box[1]+30), 5)

        # print(self.hp)

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
                    # print('reloading')
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
        self.power = 5
        self.projectile = HealingShot
        # print(self.middle)
        self.scale_img()
        # print(self.middle)


class Projectile(pygame.sprite.Sprite):
    def __init__(self, start, target, power):
        super().__init__()
        self.power = power
        self.target = target
        self.start = start
        self.speed = 0
        self.img = ''
        self.x, self.y = start
        self.angle_change = 0
        self._facing = 'e'
        self.type = None

    def update(self):
        if self.target.hit_box[0] <= self.x <= self.target.hit_box[2] and\
            self.target.hit_box[1] <= self.y <= self.target.hit_box[3]:
            self.target.hit(self.type, self.power)
            self.kill()

        if self.x < self.target.x:
            self.x += self.speed
        else:
            self.x -= self.speed

        if self.y < self.target.y:
            self.y += self.speed
        else:
            self.y -= self.speed


    def draw(self, screen):
        screen.blit(self.img, (self.x, self.y))

    @property
    def facing(self):
        return self._facing

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


class HealingShot(Projectile):
    def __init__(self, start, target, power):
        super().__init__(start, target, power)
        self.speed = 4
        self.img = pygame.image.load('lib/images/healingshot.png')
        self.type = 'HEAL'


class Handle:
    def __init__(self, location):
        self.active = False
        self.custom_hit_box = 25, 50
        self.x, self.y = location
        self._handle = pygame.image.load("lib/images/handle.png")

    def check(self, mouse_position):
        if self.hit_box[0] <= mouse_position[0] <= self.hit_box[2] and\
                self.hit_box[1] <= mouse_position[1] <= self.hit_box[3]:
                    self.active = not self.active
                    if self.active:
                        self.x -= 100
                    else:
                        self.x += 100
                    # print('CLICKED', self.active)

    def draw(self, screen):
        screen.blit(self._handle, (self.x, self.y))

    @property
    def hit_box(self):
        return self.x, self.y, self.x + self.custom_hit_box[0], self.y + self.custom_hit_box[1]


class BuildMenu:
    def __init__(self, screen, screen_size: tuple, handle: Handle):
        self.screen = screen
        self.build_menu = False
        self.handle = handle
        self.screen_width, self.screen_height = screen_size
        self.custom_hit_box = 100, 300
        self.x, self.y = self.screen_width - self.custom_hit_box[0], self.screen_height/2 - self.custom_hit_box[1]/2


        self.img = pygame.image.load("lib/images/BasicMenu.png")
        self.img = pygame.transform.scale(self.img, (100, 300))

    def check_for_handle(self):
        if self.handle.active:
            pass

    def draw(self):
        if self.handle.active:
            self.screen.blit(self.img, (self.x, self.y))

    @property
    def hit_box(self):
        return self.x, self.y, self.x + self.custom_hit_box[0], self.y + self.custom_hit_box[1]


class Encyclopedia:
    def __init__(self):
        pass

    def draw(self):
        pass



if __name__ == '__main__':
    pass










