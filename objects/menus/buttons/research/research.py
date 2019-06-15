from objects.menus.buttons.buildmenubutton import BuildMenuButton
from objects.units.ally import Ally
import pygame


class Research(BuildMenuButton):
    def __init__(self, game, slot):
        super().__init__(game.screen, game.research_centre, slot, game)
        #  research format : cost, effect_param
        self.research_dict = {}
        self.research_name = ''
        self.tier = 0
        self.active = True
        self.slot = slot
        self.button_hit_box = 54, 83
        self.description = ['']
        self.longest_word = 0

    def research(self):
        try:
            research_params = self.research_dict[self.tier+1]
            if self.try_buy(research_params[0]):
                self.handle_research_param(research_params[1])
                self.tier += 1
                self.description = self.get_description()
                self.setup_description_length()
                _ = self.research_dict[self.tier+1]

        except KeyError:
            self.kill()

    def try_buy(self, cost):
        if self.game.gold_manager.gold >= cost:
            self.game.gold_manager.gold -= cost
            return True
        return False

    def draw(self):
        self.screen.blit(self.img, (self.x, self.y))
        self.write_text(self.tier+1, (self.x+2, self.y), color=(50, 50, 0))

    def handle_research_param(self, param):
        if self.research_name == 'footmancount':
            self.game.footmen_to_spawn += 1
        elif self.research_name == 'naturalregeneration':
            Ally.regeneration["power"] += 1
            if param is not None:
                Ally.regeneration["frequency"] += 1
        else:
            raise ValueError(f"Research {self.research_name} was not recognized")

    def kill(self):
        new_buttons = []
        for group in self.build_menu.buttons:
            if not group[1] == self.slot:
                new_buttons.append(group)
        self.build_menu.buttons = new_buttons
        self.build_menu.init_slot_list()

    def write_text(self, text, where, color=(0, 0, 0), size=30, int_green=False):
        writing_font = pygame.font.Font("lib/fonts/big_noodle_titling.ttf", size)
        if int_green:
            words = text.split()
            for index, word in enumerate(words):
                try:
                    word = int(word)

                    len_so_far = 0
                    for i in words[:index]:
                        len_so_far += len(i)+1
                    to_render = writing_font.render(str(word), True, (0, 255, 0))
                    self.game.screen.blit(to_render, (where[0]+len_so_far*(size/2.85), where[1]))
                    text = text.replace(str(word), "   "*len(str(word)))

                except ValueError:
                    pass

        to_render = writing_font.render(str(text), True, color)
        self.game.screen.blit(to_render, where)

    def hover(self):
        pos = pygame.mouse.get_pos()
        button_hit_box = 0+6.5*self.longest_word, 20 + 20 * len(self.description)

        pygame.draw.rect(self.game.screen, (0, 0, 0), (pos[0],
                                                          pos[1] - button_hit_box[1],
                                                          button_hit_box[0], button_hit_box[1]))

        for index, line in enumerate(self.description):
            self.write_text(line, (pos[0] + 5, pos[1] - button_hit_box[1] + 22 * index),
                            color=(255, 255, 255), size=18, int_green=True)

    def setup_description_length(self):
        self.longest_word = 0
        for word in self.description:
            if len(word) > self.longest_word:
                self.longest_word = len(word)

    def get_description(self):
        return ['']




