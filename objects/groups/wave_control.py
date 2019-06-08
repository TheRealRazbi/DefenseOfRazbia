from objects.units.enemies.grunt import Grunt
import functions


class WaveControl:
    def __init__(self, game_controller):
        self.game = game_controller
        self.screen_size = (game_controller.width, game_controller.height)
        self.arena = game_controller.arena
        self.wave = 0

    def check(self):
        if self.game.start_button_pressed and self.game.wave_done:
            self.wave += 1
            self.game.wave_done = False
            self._load_wave()

    def _load_wave(self):
        try:
            wave_units = functions.load_wave(self.wave, also_print=True)
            self.game._spawn_footman()

            for group in wave_units:
                if group[0] == 'Grunt':
                    Grunt(self.screen_size, self.arena, starting_hp_percent=group[1])
        except FileNotFoundError:
            pass
































