import pygame


class Entity:
    entities = 0

    def __init__(self):
        Entity.entities += 1
        self.position = 0, 0

    @classmethod
    def hm_entities(cls):
        return cls.entities


class BaseTile:

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

    @property
    def area(self):
        return self._position[0], self._position[1],\
                self._position[0]+BaseTile.size[0] + self._position[1]+BaseTile.size[1]

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



















