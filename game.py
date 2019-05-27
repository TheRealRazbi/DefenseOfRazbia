import functions
import objects
import pygame
import objects
import sys


class Game:
    def __init__(self, size: tuple, map_name: str):
        pygame.init()
        self.width = size[0]
        self.height = size[1]
        self.towers = []
        self.units = objects.UnitGroup()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.map_name = map_name
        self._select_track()


    def run(self):
        run = True
        clock = pygame.time.Clock()
        self.screen.fill((0, 0, 0))
        self._build_track()
        self._spawn_footman()
        self._place_tower()

        while run:

            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()


                pos = pygame.mouse.get_pos()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    print(pos)
                    pass

            self._build_track()
            self.units.move()
            self.units.draw(self.screen)
            self.t1.draw(self.screen)

            self.t1.check_for_units(self.units)
            # print(self.units)

            pygame.display.flip()

    def _spawn_footman(self):
        indent = 0
        for i in range(1):
            footman = objects.Footman('default_map', screen_size=(self.width, self.height))
            footman.change_start_point((footman.path[0][0], -indent))
            footman.add(self.units)
            indent += 150

    def _place_tower(self):
        self.t1 = objects.HealingTower((250, 250), self.screen)


    def _select_track(self):
        if self.map_name == '':
            raise ValueError("Track name not specified")

        self.track = functions.load_track(name=self.map_name)
        self.track = pygame.transform.scale(self.track, (self.width, self.height))

    def _build_track(self):
        self.screen.blit(self.track, (0, 0))

    @property
    def original_map(self):
        return functions.load_track(self.map_name)