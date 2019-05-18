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
        self.move_point = 0
        self.lerp_value = 0
        self.movement_speed = 1
        self.img = ''
        self.angle_change = 0
        self.custom_hit_box = [0, 0]
        self.rect = (0, 0)
        self._facing = 's'

    def scale_img(self):
        self.img = pygame.transform.scale(self.img, (50, 50))

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

    def move(self):
        x1, y1 = self.x, self.y
        x2, y2 = self.path[self.move_point+1]
        x, y = x2-x1, y2-y1
        if 0 < y < x:
            self.facing = 's'

        direction = 0


    def draw(self, screen):
        self.img = pygame.transform.rotate(self.img, self.angle_change)
        self.angle_change = 0
        screen.blit(self.img, (self.hit_box[0], self.hit_box[1]))

    @property
    def centred(self):
        return self.x-self.custom_hit_box[0]/2, self.y-self.custom_hit_box[1]/2

    @facing.setter
    def facing(self, direction: str):
        directions = {'n': 0, 'e': 90, 's': 180, 'w': 270}
        self.angle_change = directions[direction] - directions[self.facing]
        if self.angle_change > 180:
            self.angle_change -= 360
        if self.angle_change < -180:
            self.angle_change += 360


class Ally(Unit):
    def __init__(self, start_position, map_name):
        super().__init__(start_position, map_name)
        self.angle_change = -90


class Enemy(Unit):
    pass


class Footman(Ally):
    def __init__(self, start_position, map_name):
        super().__init__(start_position, map_name)
        self.img = pygame.image.load('lib/images/footman.png')
        self.custom_hit_box = 50, 30  # for scale 50, 50
        self.scale_img()


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



















