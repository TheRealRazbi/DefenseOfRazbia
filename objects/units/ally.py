from objects.units.unit import Unit


class Ally(Unit):
    def __init__(self, map_name, screen_size):
        super().__init__(map_name, screen_size)
