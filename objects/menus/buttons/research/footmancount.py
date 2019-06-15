import pygame
from objects.menus.buttons.research.research import Research


class FootmanCount(Research):
    def __init__(self, game, slot):
        super().__init__(game, slot)
        self.img = pygame.image.load("lib/images/icons/research/max_footman.png")
        self.img = pygame.transform.scale(self.img, (54, 76))
        self.research_dict = {1: [30, None], 2: [40, None], 3: [50, None], 4: [65, None], 5: [80, None],
                              6: [95, None], 7: [120, None]}
        self.research_name = 'footmancount'


        # self.description = ['this is really long', 'jesus', 'christ', 'LOOONG']
        self.init_description_dict()
        self.setup_description_length()


    def action(self):
        print('works')

    def init_description_dict(self):
        for i in range(7):
            self.research_dict[i+1] = self.research_dict[i+1] + [["This research will increase",
                                                                 "the max number of footmen",
                                                                  f"Current footmen: {i+3}",
                                                                  f"After upgrade footmen: {i+4}"]]
        self.description = self.get_description()

    def get_description(self):
        return self.research_dict[self.tier+1][2]



