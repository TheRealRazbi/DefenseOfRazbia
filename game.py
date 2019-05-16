import functions
import pygame
import sys


class Game:
    def __init__(self, size: tuple, map: str):
        pygame.init()
        self.width = size[0]
        self.height = size[1]
        self.towers = []
        self.units = []
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.map = map

    def run(self):
        run = True
        clock = pygame.time.Clock()
        self.screen.fill((0, 0, 0))
        self._select_track(map=self.map)
        self._build_track()

        unit = pygame.transform.scale(pygame.image.load("lib/images/unit1.png"), (25, 25))
        unit_rect = unit.get_rect()
        self.screen.blit(unit, unit_rect)

        while run:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()

                pos = pygame.mouse.get_pos()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pass


            pygame.display.flip()




    def _select_track(self, map:str=''):
        if map == '':
            raise ValueError("Track name not specified")

        self.track = functions.load_track(name=map)

    def _build_track(self):
        self.screen.blit(self.track, (0, 0))
        # self.screen.