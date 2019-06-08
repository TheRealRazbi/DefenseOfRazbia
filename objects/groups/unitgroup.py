import pygame


class UnitGroup(pygame.sprite.Group):

    def __init__(self, *args):
        super().__init__(*args)

    def general_do(self, do, *args):
        for sprite in self.sprites():
            getattr(sprite, do)(*args)

    def move(self):
        self.general_do('move')

    def draw(self, screen):
        self.general_do('draw', screen)

    def check_enemies(self):
        self.general_do('check_enemies')

    def attack_move(self):
        self.general_do('attack_move')

    def get_rects(self, besides):
        rects = []
        for sprite in self.sprites():
            if not besides == sprite:
                rects.append(sprite.real_hit_box)
        return rects
