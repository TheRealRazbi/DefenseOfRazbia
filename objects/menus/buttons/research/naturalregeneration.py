import pygame
from objects.menus.buttons.research.research import Research


class NaturalRegeneration(Research):
    def __init__(self, game, slot):
        super().__init__(game, slot)
        self.img = pygame.image.load("lib/images/icons/research/max_footman.png")
        self.img = pygame.transform.scale(self.img, (54, 76))
        self.research_dict = {1: [40, None], 2: [60, None], 3: [50, None], 4: [65, None], 5: [80, None],
                              6: [95, None], 7: [120, None]}
        self.research_name = 'naturalregeneration'


        self.init_description_dict()
        self.setup_description_length()


    def action(self):
        print('works')

    def init_description_dict(self):
        for i in range(7):
            self.research_dict[i+1] = self.research_dict[i+1] + [["This research will increase",
                                                                 "the regeneration of footmen",
                                                                  f"Current: {i} every {i//5+2}   seconds",
                                                                  f"After: {i+1} every {i//5+2}   seconds"]]
        self.description = self.get_description()

    def get_description(self):
        return self.research_dict[self.tier+1][2]
















