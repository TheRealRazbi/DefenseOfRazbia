import pygame
import functions


class StartRoundButton:
    def __init__(self, game):
        self.game = game
        self.x, self.y = self.game.width-200, int(self.game.height / 1.8)
        self.img = pygame.image.load('lib/images/play-button.png')
        self.img_pressed = pygame.image.load('lib/images/play-button-pressed.png')
        self.custom_hit_box = 50, 50
        self.img = pygame.transform.scale(self.img, self.custom_hit_box)
        self.img_pressed = pygame.transform.scale(self.img_pressed, self.custom_hit_box)
        self.pressed = False

    def draw(self):
        if self.pressed:
            self.game.screen.blit(self.img_pressed, (self.x, self.y))
        else:
            self.game.screen.blit(self.img, (self.x, self.y))

    @property
    def rect_hit_box(self):
        return self.x, self.y, self.custom_hit_box[0], self.custom_hit_box[1]

    @property
    def hit_box(self):
        return self.x, self.y, self.custom_hit_box[0]+self.x, self.custom_hit_box[1]+self.y

    def check_click(self, click):
        if functions.clicked_in_a_box(self.hit_box, click):
            self.pressed = True




