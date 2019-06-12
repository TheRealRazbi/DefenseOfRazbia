import pygame
from objects.menus.buttons.research.research import Research


class FootmanCount(Research):
    def __init__(self, game, slot):
        super().__init__(game, slot)
        self.img = pygame.image.load("lib/images/icons/research/max_footman.png")
        self.img = pygame.transform.scale(self.img, (54, 76))
        self.research_dict = {1: [30, None], 2: [40, None], 3: [50, None]}
        self.research_name = 'footmancount'

    def action(self):
        print('works')





