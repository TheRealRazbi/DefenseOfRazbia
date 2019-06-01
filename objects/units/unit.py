from objects.units.entity import Entity
import functions
import pygame


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
