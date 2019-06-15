from objects.menus.buildmenu import BuildMenu
import pygame
import functions
import asyncio


class ResearchCentre(BuildMenu):
    def __init__(self, game, handle):
        super().__init__(game.screen, (game.width, game.height), handle, None)
        self.game = game
        self.img = pygame.image.load("lib/images/research.png")
        self.img = pygame.transform.scale(self.img, (250, 250))
        self.x, self.y = 0, (game.height-300)/2
        self.custom_hit_box = 0, 0
        self.handle.moving += 150
        self.handle.rotate()
        self.buttons_pos = []
        self.init_slot()
        self.slots = []

    def add(self, button, slot):
        self.buttons.append([button, slot])
        self.init_slot_list()

    def init_slot_list(self):
        slots = []
        for group in self.buttons:
            for index, slot in enumerate(group):
                if index % 2:
                    slots.append(slot)
        self.slots = slots

    def init_slot(self):
        for x in range(4):
            for y in range(3):
                self.buttons_pos.append((self.x + 54 * x + 5, self.y + 83 * y + 5))

    def slot(self, slot, button, coordinates_only=False):
        if not coordinates_only:
            self.add(button, slot)
        return self.buttons_pos[slot]

    def check_clicks(self, click):
        if self.handle.active:

            for slot in self.slots:
                x, y = self.slot(slot, 0, coordinates_only=True)
                hit_box = x, y, x+54, y+83
                if hit_box[0] <= click[0] <= hit_box[2] and \
                        hit_box[1] <= click[1] <= hit_box[3]:
                    for group in self.buttons:
                        for index, current in enumerate(group):
                            if index % 2:
                                if current == slot:
                                        group[0].research()

    def hover(self, pos):
        if self.handle.active:
            for slot in self.slots:
                x, y = self.slot(slot, 0, coordinates_only=True)
                hit_box = x, y, x + 54, y + 83

                if functions.clicked_in_a_box(hit_box, pos):
                    self.button(slot).hover()








