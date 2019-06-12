from objects.menus.buttons.buildmenubutton import BuildMenuButton
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

    def research(self):
        try:
            research_params = self.research_dict[self.tier+1]
            if self.try_buy(research_params[0]):
                self.handle_research_param(research_params[1])
                self.tier += 1
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
            self.game.arena.get_footman_to_spawn()
        else:
            raise ValueError("Research has no name")

    def kill(self):
        new_buttons = []
        for group in self.build_menu.buttons:
            if not group[1] == self.slot:
                new_buttons.append(group)
        self.build_menu.buttons = new_buttons
        self.build_menu.init_slot_list()

    def write_text(self, text, where, color=(0, 0, 0), size=30):
        writing_font = pygame.font.Font("lib/fonts/big_noodle_titling.ttf", size)

        to_render = writing_font.render(str(text), True, color)
        self.game.screen.blit(to_render, where)










