import pygame


class Projectile(pygame.sprite.Sprite):
    def __init__(self, start, target, power):
        super().__init__()
        self.power = power
        self.target = target
        self.start = start
        self.speed = 0
        self.img = ''
        self.x, self.y = start
        self.angle_change = 0
        self._facing = 'e'
        self.type = None

    def update(self):
        if self.target.hit_box[0] <= self.x <= self.target.hit_box[2] and\
                self.target.hit_box[1] <= self.y <= self.target.hit_box[3]:
            self.target.hit(self.type, self.power)
            self.kill()

        if self.x < self.target.x:
            self.x += self.speed
        else:
            self.x -= self.speed

        if self.y < self.target.y:
            self.y += self.speed
        else:
            self.y -= self.speed

    def draw(self, screen):
        screen.blit(self.img, (self.x, self.y))

    @property
    def facing(self):
        return self._facing

    @facing.setter
    def facing(self, direction):
        directions = {'n': 0, 'e': 90, 's': 180, 'w': 270}
        self.angle_change = directions[direction] - directions[self.facing]
        if self.angle_change > 180:
            self.angle_change -= 360
        if self.angle_change < -180:
            self.angle_change += 360

        self.img = pygame.transform.rotate(self.img, self.angle_change)
        self.angle_change = 0

        self._facing = direction
