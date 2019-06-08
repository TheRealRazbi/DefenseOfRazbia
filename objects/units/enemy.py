from objects.units.unit import Unit


class Enemy(Unit):
    team = 1

    def __init__(self, screen_size, arena):
        super().__init__(screen_size, arena)
        self.enemies = self.arena.ally_units
        self.team = 1
        self.movement_speed = 2

    def enter_arena(self):
        self.tp_to_arena()





