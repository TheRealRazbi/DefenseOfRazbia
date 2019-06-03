from objects.units.unit import Unit
import functions


class Ally(Unit):
    def __init__(self, map_name, screen_size):
        super().__init__(screen_size)
        self.path = functions.load_path(map_name, scaling=screen_size)
        self.team = 0








