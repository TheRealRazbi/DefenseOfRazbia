from objects.projectiles.projectile import Projectile
import pygame


class GoldShot(Projectile):
    def __init__(self, start, target, power):
        super().__init__(start, target, power)
        self.speed = 4
        self.img = pygame.image.load('lib/images/goldshot.png')
        # self.img = pygame.transform(self.img, (10, 10))
        self.type = 'TRASMUTE'
