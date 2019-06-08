from objects.units.enemy import Enemy
import pygame


class Grunt(Enemy):
    def __init__(self, screen_size, enemy_group, arena):
        super().__init__(screen_size, enemy_group, arena)
        self.img = pygame.image.load("lib/images/grunt_missing_texture.png")
        self.custom_hit_box = 50, 30
        self.img = pygame.transform.scale(self.img, self.custom_hit_box)

        self.hp = self.max_hp / 2
        self.x = 0
        self.y = 0
        self.arena.tp_to_arena(self)
        self.add(self.arena.enemy_units)


    # def draw(self, screen):
    #     screen.blit(self.img, (self.x, self.y))



















