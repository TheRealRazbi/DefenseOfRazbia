import pygame
import functions


class FastForwardButton:
    def __init__(self, game):
        self.game = game
        self.x, self.y = self.game.width-300, int(self.game.height / 1.8)
        self.img = pygame.image.load('lib/images/fast_forward.png')
        self.img_pressed = pygame.image.load('lib/images/fast_forward-pressed.png')
        self.img_pressed2 = pygame.image.load('lib/images/fast_forward-pressed2.png')
        self.custom_hit_box = 50, 50
        self.img = pygame.transform.scale(self.img, self.custom_hit_box)
        self.img_pressed = pygame.transform.scale(self.img_pressed, self.custom_hit_box)
        self.img_pressed2 = pygame.transform.scale(self.img_pressed2, self.custom_hit_box)
        self.pressed = 0
        self.font_text = pygame.font.Font('lib/fonts/big_noodle_titling.ttf', 25)

    def draw(self):
        if self.pressed == 1:
            self.game.screen.blit(self.img_pressed, (self.x, self.y))
        elif self.pressed == 0:
            self.game.screen.blit(self.img, (self.x, self.y))
        elif self.pressed == 2:
            self.game.screen.blit(self.img_pressed2, (self.x, self.y))

        ff_font_to_draw = self.font_text.render(str(self.pressed), True, (0, 0, 0))
        self.game.screen.blit(ff_font_to_draw, (self.x+self.custom_hit_box[0]/2, self.y-self.custom_hit_box[1]/2))

    @property
    def rect_hit_box(self):
        return self.x, self.y, self.custom_hit_box[0], self.custom_hit_box[1]

    @property
    def hit_box(self):
        return self.x, self.y, self.custom_hit_box[0]+self.x, self.custom_hit_box[1]+self.y

    def check_click(self, click):
        if functions.clicked_in_a_box(self.hit_box, click):
            self.pressed += 1
            if self.pressed > 2:
                self.pressed = 0



