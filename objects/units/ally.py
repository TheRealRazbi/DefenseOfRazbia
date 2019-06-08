from objects.units.unit import Unit
import functions


class Ally(Unit):
    team = 0

    def __init__(self, map_name, screen_size, arena):
        super().__init__(screen_size, arena)
        self.enemies = self.arena.enemy_units
        self.path = functions.load_path(map_name, scaling=screen_size)
        self.team = 0








