import pygame


class TowerGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def draw(self, screen):
        for sprite in self.sprites():
            sprite.draw(screen)

    def check_for_units(self, units):
            for sprite in self.sprites():
                sprite.check_for_units(units)

    @property
    def projectile_group(self):
        res = []
        for sprite in self.sprites():
            res.append(sprite.projectile_group)
        return res

    def projectile_group_empty(self):
        for sprite in self.sprites():
            sprite.projectile_group.empty()

    def check_click(self, click):
        for sprite in self.sprites():
            sprite.check_click(click)

    def deselect(self):
        for sprite in self.sprites():
            sprite.selected = False

    def try_to_select(self, current_sprite):
        for sprite in self.sprites():
            if sprite == current_sprite:
                sprite._selected = True
            else:
                sprite._selected = False






