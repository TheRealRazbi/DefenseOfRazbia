from objects.projectiles.projectile import Projectile
import pygame


class HealingShot(Projectile):
    def __init__(self, start, target, power):
        super().__init__(start, target, power)
        self.speed = 4
        self.img = pygame.image.load('lib/images/healingshot.png')
        self.type = 'HEAL'
