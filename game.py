from functions import load_track, build_unit_track, build_base_track
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
        self.clicks = []

    def run(self):
        run = True

        self.screen.fill((0, 0, 0))
        self._select_track(map=self.map)
        self._build_track()
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()

                pos = pygame.mouse.get_pos()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.clicks.append(pos)
                    print(self.clicks)

            pygame.display.flip()




    def _select_track(self, map:str=''):
        if map == '':
            raise ValueError("Track name not specified")

        self.track = load_track(name=map)

    def _build_track(self):
        self.screen.blit(self.track, (0, 0))
        # self.screen.