import pygame


class Handle:
    def __init__(self, location):
        self.active = False
        self.custom_hit_box = 25, 50
        self.x, self.y = location
        self._handle = pygame.image.load("lib/images/handle.png")

    def check(self, mouse_position):
        if self.hit_box[0] <= mouse_position[0] <= self.hit_box[2] and\
                self.hit_box[1] <= mouse_position[1] <= self.hit_box[3]:
                    self.active = not self.active
                    if self.active:
                        self.x -= 100
                    else:
                        self.x += 100

    def draw(self, screen):
        screen.blit(self._handle, (self.x, self.y))

    @property
    def hit_box(self):
        return self.x, self.y, self.x + self.custom_hit_box[0], self.y + self.custom_hit_box[1]