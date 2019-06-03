import pygame


class Arena:
    def __init__(self, screen, screen_size, units):
        self.width, self.height = screen_size
        self.img = pygame.image.load('lib/images/arena.png')
        self.screen = screen
        self.units = units


    def draw(self):
        self.screen.blit(self.img, (0, self.height-300))
        self.units.draw()









