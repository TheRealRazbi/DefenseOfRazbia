from objects.units.entity import Entity
import functions
import pygame
import math
from collections import deque


class Unit(Entity):
    regeneration = {"frequency": 0.5, "ready": 0, "power": 0}

    def __init__(self, screen_size, arena):
        super().__init__()
        self.arena = arena
        self.enemies = []
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
        self.aggro_range = 100
        self.attack_range = self.custom_hit_box[0]+self.custom_hit_box[1] + 60
        self.attack_cooldown = 0
        self.attack_speed = 2
        self.attack_damage = 1
        self.closest_enemy = deque(maxlen=1)
        self.closest_enemy.append([0, self.aggro_range*10])
        self.enemies_found = [[999, self.aggro_range*10]]
        self.in_arena = False
        self.team = -1
        self.walking_animation = False
        self.img_move = []
        self.standing = False
        self.fighting = False

    def check_enemies(self):
        for enemy in self.enemies:
            distance = int(math.sqrt(abs(enemy.real_hit_box[0] - self.real_hit_box[0])**2 +
                                 abs(enemy.real_hit_box[1] - self.real_hit_box[1])**2))

            if distance < self.aggro_range:
                # print(f'{enemy} fOUND')
                # pygame.time.wait(9999)
                in_group = False
                for index, group in enumerate(self.enemies_found):
                    if enemy in group:
                        self.enemies_found[index] = [enemy, distance]
                        in_group = True

                if not in_group:
                    self.enemies_found.append([enemy, distance])

                for group in self.enemies_found:
                    if self.closest_enemy[0][1] > group[1]:
                        self.closest_enemy.append([enemy, distance])
                        # print(f'{enemy} is the new closest to {self}, because {self.closest_enemy[0][1]}>{group[1]}')

                return self.closest_enemy

    def _check_collision(self, change):
        hit_box = self.real_hit_box[0]+change[0], self.real_hit_box[1]+change[1], self.real_hit_box[2], self.real_hit_box[3]
        hit_box = pygame.rect.Rect(hit_box)

        unit_rects = self.arena.all_units.get_rects(self)
        if hit_box.collidelist(unit_rects) >= 0:
            # print(f'{self} collided ')
            return True
        return False

    def attack_move(self):
        move_to_destination = True
        destination = [self.arena.check_point[self.team][0],
                        self.arena.check_point[self.team][1],
                        30, 30]
        arena_destination = destination

        closest_enemy = self.check_enemies()
        if closest_enemy is not None:
            destination[0] = closest_enemy[0][0].real_hit_box[0]
            destination[1] = closest_enemy[0][0].real_hit_box[1]
            destination[2] = closest_enemy[0][0].custom_hit_box[0]
            destination[3] = closest_enemy[0][0].custom_hit_box[1]

            if closest_enemy[0][0].alive():
                if closest_enemy[0][1] < self.attack_range:
                    self.standing = True
                    move_to_destination = False
                    if self.attack_cooldown <= 0:
                        closest_enemy[0][0].hit('DAMAGE', self.attack_damage)
                        self.attack_cooldown += self.arena.game.target_fps/self.attack_speed
                        # print('damaging')
                    else:
                        self.attack_cooldown -= 1
                        # print('NOT READY YET')

        if closest_enemy is not None and not closest_enemy[0][0].alive():
            # print('DEAD')
            self.closest_enemy.append([0, self.aggro_range * 10])
            move_to_destination = True

            # print(f'{closest_enemy[0][1]} < {self.attack_range}')
        if move_to_destination:
            if self.real_hit_box.colliderect(destination) and destination == arena_destination:
                pass
                self.standing = True
                self.arena.wave_done = True
                self.arena.clear()
                # print(self.arena.ally_units)

                if self.team == 0:
                    print('TEAM 1 WON WOO')
                    self.arena.game.gold_manager.gold += 10*self.arena.game.wave_control.wave
                elif self.team == 1:
                    self.arena.game.lives_manager.damage(self.attack_damage*self.hp)
                    print('enemies won , Feelsbadman')
                # print(f'{self} arrived at {destination}, and his position is {self.x} {self.y}')
            else:
                pass
                definitely_moving = False

                x_change, _ = functions.move_towards_an_area((self.x, self.y), destination, self.movement_speed,
                                                             move_y=False)

                if not self._check_collision((x_change, 0)):
                    self.x += x_change
                    if x_change != 0:
                        definitely_moving = True

                _, y_change = functions.move_towards_an_area((self.x, self.y), destination, self.movement_speed,
                                                                    move_x=False)

                if not self._check_collision((0, y_change)):
                    self.y += y_change
                    if y_change != 0:
                        definitely_moving = True

                self.standing = not definitely_moving
                    # print(f"{self}, can't move to {self.x, self.y}")

    def hit(self, power_type, power):
        if power_type == 'HEAL':
            if self.hp < self.max_hp:
                self.hp += power
                if self.hp > self.max_hp:
                    self.hp = self.max_hp
        elif power_type == 'DAMAGE':
            self.hp -= power
            if self.hp < 0:
                self.kill()
        elif power_type == "TRASMUTE":
            self.arena.game.gold_manager.gold += power

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
        return pygame.rect.Rect(self.centred[0], self.centred[1],
                self.centred[0]+self.custom_hit_box[0],
                self.centred[1]+self.custom_hit_box[1])

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
            except IndexError:
                self.moveable = False
                self.tp_to_arena()

    def tp_to_arena(self):
        self.movement_speed = 2  # line added to made testing easier
        self.standing = True
        self.kill()
        self.in_arena = True
        self.arena.tp_to_arena(self)
        if self.team == 0:
            self.facing = 'e'
            self.add(self.arena.ally_units)
        elif self.team == 1:
            self.facing = 'w'
            self.add(self.arena.enemy_units)

    def _draw_aggro_range(self, screen):
        pygame.draw.circle(screen, (0, 0, 0), (int(self.x), int(self.y)), self.aggro_range, 3)

    def _draw_attack_range(self, screen):
        pygame.draw.circle(screen, (0, 0, 0), (int(self.x), int(self.y)), self.attack_range, 3)

    def _draw_hp_bar(self, screen):
        hp_percent = (30 * (self.hp / self.max_hp)) - 15

        pygame.draw.line(screen, (255, 255, 255), (self.x-15, self.centred[1]+self.custom_hit_box[1]*1.5),
                                                (self.x+15, self.centred[1]+self.custom_hit_box[1]*1.5), 5)

        pygame.draw.line(screen, (0, 255, 0), (self.x-15, self.centred[1]+self.custom_hit_box[1]*1.5),
                                                (self.x+hp_percent, self.centred[1]+self.custom_hit_box[1]*1.5), 5)

    def _draw_hit_box(self, screen):
        how_red = 255
        pygame.draw.rect(screen, (how_red, how_red, how_red), self.real_hit_box, 2)

    def _select_image(self):
        if not self.standing:
            frames_per_image = int(20 / self.movement_speed)
            if self.move_count + 1 >= len(self.img_move)*frames_per_image:
                self.move_count = 0

            if self.walking_animation:
                try:
                    self.img = self.img_move[self.move_count//frames_per_image]
                except ZeroDivisionError:
                    frames_per_image += 1
                    self.img = self.img_move[self.move_count//frames_per_image]
                self.move_count += 1
        elif self.img_stand != '':
            self.img = self.img_stand

    def draw(self, screen):
        self._select_image()
        if self.in_arena:
            screen.blit(self.img, (self.real_hit_box[0], self.real_hit_box[1]))
        else:
            screen.blit(self.img, (self.centred[0], self.centred[1]))
        self._draw_hp_bar(screen)
        # self._draw_hit_box(screen)
        # self._draw_aggro_range(screen)

    @property
    def centred(self):
        return self.x-self.custom_hit_box[0]/2, self.y-self.custom_hit_box[1]/2

    @property
    def real_hit_box(self):
        return pygame.rect.Rect(self.centred[0], self.centred[1], self.custom_hit_box[0], self.custom_hit_box[1])

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

    def regenerate(self):
        if self.regeneration["ready"] < 1:
            self.regeneration["ready"] += (1 / self.arena.game.target_fps) * self.regeneration["frequency"]
        else:
            if self.hp+self.regeneration["power"] < self.max_hp:
                self.hp += self.regeneration["power"]
                self.regeneration["ready"] = 0
            else:
                self.hp = self.max_hp



