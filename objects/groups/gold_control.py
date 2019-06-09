import pygame


class GoldControl:
    def __init__(self, game):
        self.game = game
        self._gold = 5000
        self.img = pygame.image.load("lib/images/coin.png")
        self.custom_hit_box = 50, 50
        self.img = pygame.transform.scale(self.img, self.custom_hit_box)
        self.x, self.y = self.game.width-200, 20
        self.gold_font = pygame.font.Font('lib/fonts/big_noodle_titling.ttf', 50)
        pygame.font.init()

    def draw(self):
        self.game.screen.blit(self.img, (self.x, self.y))
        pygame.draw.rect(self.game.screen, (255, 255, 255), (self.x+self.custom_hit_box[0]+1, self.y,
                                            self.custom_hit_box[0]-25+18*(len(str(self.gold))-1),
                                            self.custom_hit_box[1]))
        gold_font_to_draw = self.gold_font.render(str(self.gold), True, (0, 0, 0))
        self.game.screen.blit(gold_font_to_draw, (self.x+self.custom_hit_box[0]+2, self.y))
        # self.game.screen.blit(gold_font_to_draw, (100, 100))

    @property
    def gold(self):
        return self._gold

    @gold.setter
    def gold(self, amount):
        self._gold = int(amount)






