from objects.units.entity import Entity
import functions
import pygame
import math


class Unit(Entity):
    def __init__(self, screen_size, enemy_group, arena):
        super().__init__()
        self.arena = arena
        self.enemies = enemy_group
        self.path = [[0, 0]]
        self.x = self.path[0][0]
        self.y = self.path[0][1]
        self.x_ratio = screen_size[0] / 800
        self.y_ratio = screen_size[1] / 600
        self.prev_x = self.x
        self.prev_y = self.y
        self.move_point = 0
        self.move_count = 0
        self.movement_speed = 2 * ((self.x_ratio + self.y_ratio)/2)
        self.img = ''
        self.img_stand = ''
        self.angle_change = 0
        self.custom_hit_box = [0, 0]
        self.rect = (0, 0)
        self.max_hp = 100
        self.hp = 1
        self._facing = 'e'
        self.moveable = True
        self.choose_facing = True
        self.agro_range = 50
        self.attack_range = 20
        self.in_arena = False
        self.team = -1
        self.walking_animation = False
        self.img_move = []
        self.standing = False
        self.fighting = False

    def check_enemies(self):
        for enemy in self.enemies:
            distance = math.sqrt(abs(enemy.x - self.x)**2 + abs(enemy.y - self.y)**2)

            if distance < self.agro_range:
                print(f'{enemy} fOUND')

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
        if self.walking_animation:
            for index, image in enumerate(self.img_move):
                self.img_move[index] = pygame.transform.scale(image, size)
            if self.img_stand != '':
                self.img_stand = pygame.transform.scale(self.img_stand, size)

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
            # self._select_image()

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
        self.standing = True
        self.kill()
        self.facing = 'e'
        self.in_arena = True
        self.arena.tp_to_arena(self)
        if self.team == 0:
            self.add(self.arena.ally_units)
        elif self.team == 1:
            self.add(self.arena.enemy_units)

    def _draw_hp_bar(self, screen):
        hp_percent = (30 * (self.hp / self.max_hp)) - 15

        pygame.draw.line(screen, (255, 255, 255), (self.x-15, self.centred[1]+self.custom_hit_box[1]+30),
                                            (self.x+15, self.centred[1]+self.custom_hit_box[1]+30), 5)

        pygame.draw.line(screen, (0, 255, 0), (self.x-15, self.centred[1]+self.custom_hit_box[1]+30),
                                            (self.x+hp_percent, self.centred[1]+self.custom_hit_box[1]+30), 5)

    def _select_image(self):
        if not self.standing:
            frames_per_image = int(20 / self.movement_speed)
            if self.move_count + 1 >= len(self.img_move)*frames_per_image:
                self.move_count = 0

            if self.walking_animation:
                self.img = self.img_move[self.move_count//frames_per_image]
                self.move_count += 1
        elif self.img_stand != '':
            self.img = self.img_stand


    def draw(self, screen):
        self._select_image()
        screen.blit(self.img, (self.hit_box[0], self.hit_box[1]))
        self._draw_hp_bar(screen)

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
        for index, img in enumerate(self.img_move):
            self.img_move[index] = pygame.transform.rotate(img, self.angle_change)
        if self.img_stand is not '':
            self.img_stand = pygame.transform.rotate(self.img_stand, self.angle_change)
        self.angle_change = 0

        self._facing = direction

