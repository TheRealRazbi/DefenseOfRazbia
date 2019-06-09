import pygame
from objects.menus.handle import Handle
import math


class BuildMenu:
    def __init__(self, screen, screen_size: tuple, handle: Handle, tower_group):
        self.tower_group = tower_group
        self.screen = screen
        self.build_menu = False
        self.handle = handle
        self.screen_width, self.screen_height = screen_size
        self.custom_hit_box = 100, 300
        self.x, self.y = self.screen_width - self.custom_hit_box[0], self.screen_height/2 - self.custom_hit_box[1]/2
        self.buttons = []

        self.img = pygame.image.load("lib/images/BasicMenu.png")
        # self.img = pygame.transform.scale(self.img, (100, 300))

    def check_clicks(self, click):
        if self.handle.active:
            slots = []
            for group in self.buttons:
                for index, slot in enumerate(group):
                    if index % 2:
                        slots.append(slot)

            for slot in slots:
                x, y = self.slot(slot, 0, coordinates_only=True)
                hit_box = x, y, x+37, y+37
                if hit_box[0] <= click[0] <= hit_box[2] and \
                        hit_box[1] <= click[1] <= hit_box[3]:
                    for group in self.buttons:
                        for index, current in enumerate(group):
                            if index % 2:
                                if current == slot:
                                        group[0].action()

    def draw(self):
        if self.handle.active:
            self.screen.blit(self.img, (self.x, self.y))
            for group in self.buttons:
                for index, button in enumerate(group):
                    if index % 2:
                        pass
                    else:
                        button.draw()

    @property
    def hit_box(self):
        return self.x, self.y, self.x + self.custom_hit_box[0], self.y + self.custom_hit_box[1]

    def slot(self, slot, button, coordinates_only=False):
        slots = []
        for i in range(14):
            if i % 2:
                to_add = 57
                temp = [self.x + to_add, self.y - 37 + (math.ceil(i / 2) * 47)]

            else:
                to_add = 10
                temp = [self.x + to_add, self.y + 10 + (math.ceil(i / 2) * 47)]

            slots.append(temp)

        if not coordinates_only:
            self.add(button, slot)
        return slots[slot]

    def is_button_active(self, slot):
        for group in self.buttons:
            if group[1] == slot:
                active = group[0].active
                return active
        raise ValueError(f"Button on slot {slot} doesn't exist")

    def add(self, button, slot):
        self.buttons.append([button, slot])

    def button(self, slot):
        for group in self.buttons:
            if group[1] == slot:
                return group[0]

