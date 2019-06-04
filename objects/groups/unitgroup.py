import pygame


class UnitGroup(pygame.sprite.Group):
    def __init__(self, *args):
        super().__init__(*args)

    def move(self):
        for sprite in self.sprites():
            sprite.move()

    def draw(self, screen):
        for sprite in self.sprites():
            sprite.draw(screen)

    def check_enemies(self):
        for sprite in self.sprites():
            sprite.check_enemies()