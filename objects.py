import pygame
import functions
import math


class Entity:
    entities = 0

    def __init__(self):
        Entity.entities += 1
        self.position = 0, 0

    @classmethod
    def hm_entities(cls):
        return cls.entities


class Unit(Entity):
    def __init__(self, start_position, map_name):
        super().__init__()
        self.start_position = start_position
        self.path = functions.load_path(map_name)
        self.x = self.path[0][0]
        self.y = self.path[0][1]
        self.path_pos = 0
        self.move_count = 0
        self.move_dis = 0
        self.dis = 0
        self.img = ''

    def move(self):
        x1, y1 = self.path[self.path_pos]
        if self.path_pos + 1 >= len(self.path):
            x2, y2 = 810, 396
        else:
            x2, y2 = self.path[self.path_pos+1]

        move_dis = math.sqrt((x2-x1)**2 + (y2-y1)**2)


        self.move_count += 1
        dirn = (x2 - x1, y2 - y1)

        move_x, move_y = (self.x + dirn[0] * self.move_count, self.y + dirn[1] * self.move_count)
        self.dis += math.sqrt((move_x-x1)**2 + (move_y-y1)**2)

        # Go to the next point
        if self.dis >= move_dis:
            self.dis = 0
            self.move_count = 0
            self.path_pos += 1
            if self.path_pos >= len(self.path):
                return False

        self.x = move_x
        self.y = move_y
        return True

    def draw(self, screen):
        screen.blit(self.img, (self.x, self.y))


class Ally(Unit):
    pass


class Enemy(Unit):
    pass


class BaseTile:
    tiles = 0
    size = 10, 10

    def __init__(self, position: tuple):
        if len(position) != 2:
            raise ValueError("A number other than 2 was used to create a tile ")
        if position[0] < 0 or position[1] < 0:
            raise ValueError(f"Invalid coordonates . Coordonates used {position}")
        try:
            position = tuple(position)
        except Exception as e:
            print("Can't convert to tuple", e)

        self._position = position
        self._image_name = 'basetile.png'
        self._image_dir = 'lib/images/'
        BaseTile.tiles += 1

    @property
    def area(self):
        return self._position[0], self._position[1],\
                self._position[0]+BaseTile.size[0],  self._position[1]+BaseTile.size[1]

    @property
    def position(self):
        return self._position

    @property
    def image(self):
        return pygame.image.load(self._image_dir + self._image_name)

    def is_inside(self, coordinates: tuple):
        if self.area[0] <= coordinates[0] <= self.area[2] or self.area[1] >= coordinates[1] >= self.area[3]:
            return True
        return False


class UnitTile(BaseTile):

    def __init__(self, position):
        super().__init__(position)
        self._image_name = 'unittile.png'


class TowerTile(BaseTile):

    def __init__(self, position):
        super().__init__(position)
        self._image = 'towertile.png'


if __name__ == '__main__':
    pass



















