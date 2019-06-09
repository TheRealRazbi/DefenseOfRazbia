import pygame


class Entity(pygame.sprite.Sprite):
    entities = 0

    def __init__(self):
        super().__init__()
        Entity.entities += 1

    @classmethod
    def hm_entities(cls):
        return cls.entities
