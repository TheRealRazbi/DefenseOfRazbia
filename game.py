from functions import load_track, build_unit_track, build_base_track
import pygame
import sys


class Game:
    def __init__(self, size: tuple, track_name: str):
        pygame.init()
        self.width = size[0]
        self.height = size[1]
        self.towers = []
        self.units = []
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.track_name = track_name

    def run(self):
        run = True

        self._select_track(track_name=self.track_name)
        self._build_track()
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
            pygame.display.flip()

    def _select_track(self, track_name:str=''):
        if track_name == '':
            raise ValueError("Track name not specified")

        self.track = load_track(name=track_name)

    def _build_track(self):
        build_base_track((self.width, self.height), self.screen)
        build_unit_track(self.track, self.screen)