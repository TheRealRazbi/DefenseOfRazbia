import pygame


class ProjectileGroup(pygame.sprite.Group):
    def __init__(self, *args):
        super().__init__(*args)

    def draw(self, screen):
        for sprite in self.sprites():
            sprite.draw(screen)
